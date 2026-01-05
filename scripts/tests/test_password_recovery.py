from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, PasswordResetToken
from app.core.security import verify_password
import uuid

client = TestClient(app)

def test_password_recovery_flow():
    """
    Testa o fluxo completo de recuperação de senha:
    1. Solicitação de token (Forgot Password).
    2. Verificação do token no banco.
    3. Redefinição da senha (Reset Password).
    4. Login com a nova senha.
    """
    # 1. Setup
    unique_id = uuid.uuid4().hex[:6]
    email = f"recover-{unique_id}@test.com"
    old_pass = "oldpass123"
    new_pass = "newpass123"
    
    db = SessionLocal()
    company = Company(
        name="Recover Corp",
        slug=f"rec-{unique_id}",
        owner_email=email,
        password_hash="hash_invalido" # Vamos resetar isso
    )
    db.add(company)
    db.commit()
    db.close()

    # 2. Solicitar Recuperação
    res_forgot = client.post("/api/auth/forgot-password", json={"email": email})
    assert res_forgot.status_code == 200
    
    # 3. Pegar o token do banco (Simulando acesso ao e-mail)
    db = SessionLocal()
    token_entry = db.query(PasswordResetToken).filter(PasswordResetToken.user_email == email).first()
    assert token_entry is not None
    assert token_entry.used is False
    token = token_entry.token
    db.close()

    # 4. Redefinir Senha
    res_reset = client.post("/api/auth/reset-password", json={
        "token": token,
        "new_password": new_pass
    })
    assert res_reset.status_code == 200
    assert res_reset.json()["message"] == "Senha alterada com sucesso"

    # 5. Verificar Login com Nova Senha
    res_login = client.post("/api/auth/token", data={
        "username": email,
        "password": new_pass
    })
    assert res_login.status_code == 200
    assert "access_token" in res_login.json()
    
    # 6. Verificar se token foi marcado como usado
    db = SessionLocal()
    token_entry = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    assert token_entry.used is True
    db.close()