import sys
import os
from pathlib import Path

# [BOILERPLATE: Injeção de Path para localizar o pacote 'app']
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession
from app.core.security import create_access_token
import uuid

client = TestClient(app)

def test_table_open_broadcast_integrity():
    """
    Valida se o backend dispara o broadcast via WebSocket ao abrir uma mesa.
    Isso garante que o Mobile POS receba o sinal de sincronização.
    """
    db = SessionLocal()
    try:
        # 1. Setup
        uid = uuid.uuid4()
        email = f"sync-{uid.hex[:6]}@test.com"
        company = Company(id=uid, name="Sync Test", slug=f"sync-{uid.hex[:6]}", owner_email=email)
        db.add(company)
        db.commit()
        
        table = Table(company_id=company.id, table_number=99, qr_token="token-sync")
        db.add(table)
        db.commit()

        token = create_access_token(data={"sub": email, "role": "owner", "account_type": "company"})
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Mock do WebSocket Manager
        with patch("app.routers.admin_tables.manager.broadcast", new_callable=AsyncMock) as mock_broadcast:
            # 3. Ação: Abrir Mesa
            res = client.post(f"/api/admin/tables/{table.id}/open", headers=headers, json={"customer_name": "Realtime User"})
            assert res.status_code == 200

            # 4. Validação do Broadcast
            assert mock_broadcast.called
            args, _ = mock_broadcast.call_args
            message = args[0]
            
            # O mobile espera 'order_update' para disparar o triggerTableRefresh()
            assert message["type"] == "order_update"
            assert "table_id" in message
            print(f"\n✅ Broadcast de mesa validado: {message}")

    finally:
        db.close()

if __name__ == "__main__":
    test_table_open_broadcast_integrity()
