from sqlalchemy.orm import Session
from fastapi import Request
from app.models import AuditLog, AuditAction, Company, Employee
from typing import Any, Optional
import json
from decimal import Decimal
from datetime import datetime, time

class AuditService:
    @staticmethod
    def log(
        db: Session,
        user: Any, # Company ou Employee
        action: AuditAction,
        resource: str,
        resource_id: str,
        details: Optional[dict] = None,
        request: Optional[Request] = None
    ):
        """
        Registra uma ação no log de auditoria.
        Falhas no log não devem impedir a ação principal, mas devem limpar a sessão.
        """
        try:
            # Identificar quem fez a ação
            user_name = "Sistema"
            user_role = "system"
            company_id = None

            if isinstance(user, Company):
                user_name = user.name
                user_role = "owner"
                company_id = user.id
            elif isinstance(user, Employee):
                user_name = user.name
                user_role = user.role
                company_id = user.company_id
            
            if not company_id:
                return # Não loga ações sem contexto de empresa

            # Capturar IP se disponível
            ip_address = None
            if request:
                ip_address = request.client.host

            # Sanitizar JSON (Decimal/Date não serializam nativamente)
            clean_details = AuditService._sanitize_json(details) if details else None

            log_entry = AuditLog(
                company_id=company_id,
                user_name=user_name,
                user_role=user_role,
                action=action,
                resource=resource,
                resource_id=str(resource_id),
                details=clean_details,
                ip_address=ip_address
            )
            
            db.add(log_entry)
            db.commit()
            
        except Exception as e:
            print(f"⚠️ Falha não-crítica no AuditLog: {e}")
            db.rollback() # CRÍTICO: Limpa a transação falha para não quebrar o request principal

    @staticmethod
    def _sanitize_json(data: Any) -> Any:
        """Converte tipos complexos (Decimal, Date) para string/float para salvar no JSON"""
        if isinstance(data, dict):
            return {k: AuditService._sanitize_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [AuditService._sanitize_json(v) for v in data]
        elif isinstance(data, Decimal):
            return float(data)
        elif isinstance(data, (datetime, time)):
            return str(data)
        return data

    @staticmethod
    def diff(old_obj: Any, new_data: dict) -> dict:
        """
        Compara um objeto SQLAlchemy com um dicionário de novos dados
        e retorna apenas o que mudou.
        """
        changes = {"old": {}, "new": {}}
        has_changes = False

        for key, new_val in new_data.items():
            if hasattr(old_obj, key):
                old_val = getattr(old_obj, key)
                
                # Normalização para comparação
                if isinstance(old_val, Decimal):
                    old_val = float(old_val)
                    if isinstance(new_val, str):
                        try: new_val = float(new_val)
                        except: pass
                
                if old_val != new_val:
                    changes["old"][key] = old_val
                    changes["new"][key] = new_val
                    has_changes = True
        
        return changes if has_changes else None