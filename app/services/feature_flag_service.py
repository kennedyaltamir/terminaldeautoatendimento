import json
import logging
from sqlalchemy.orm import Session
from app.models import FeatureFlag
from app.core.cache import CacheService
from uuid import UUID
from typing import Union

logger = logging.getLogger("FeatureFlagService")

class FeatureFlagService:
    CACHE_TTL = 300  # 5 minutos
    CACHE_PREFIX = "flags:"

    @staticmethod
    def get_flags(db: Session, company_id: Union[str, UUID]) -> dict:
        """
        Retorna todas as flags de uma empresa.
        Prioriza o cache em Redis para performance.
        """
        comp_id_str = str(company_id)
        cache_key = f"{FeatureFlagService.CACHE_PREFIX}{comp_id_str}"

        # 1. Tentar recuperar do Cache
        cached = CacheService.get(cache_key)
        if cached:
            try:
                return json.loads(cached)
            except Exception as e:
                logger.error(f"Erro ao decodificar cache de flags para {comp_id_str}: {e}")

        # 2. Fallback para Banco de Dados
        try:
            flags = db.query(FeatureFlag).filter(FeatureFlag.company_id == company_id).all()
            flag_map = {f.key: f.is_enabled for f in flags}

            # 3. Atualizar Cache
            CacheService.set(cache_key, flag_map, ttl=FeatureFlagService.CACHE_TTL)
            return flag_map
        except Exception as e:
            logger.error(f"Erro ao buscar flags no banco para {comp_id_str}: {e}")
            return {}

    @staticmethod
    def check(db: Session, company_id: Union[str, UUID], key: str) -> bool:
        """
        Verifica se uma flag específica está ativa.
        Utilizado em lógica de negócio para ramificação de código.
        """
        flags = FeatureFlagService.get_flags(db, company_id)
        return flags.get(key, False)

    @staticmethod
    def set_flag(db: Session, company_id: Union[str, UUID], key: str, value: bool):
        """
        Ativa ou desativa uma flag para um tenant específico.
        Invalida o cache imediatamente para garantir consistência.
        """
        comp_id_str = str(company_id)
        flag = db.query(FeatureFlag).filter(
            FeatureFlag.company_id == company_id,
            FeatureFlag.key == key
        ).first()

        if not flag:
            flag = FeatureFlag(company_id=company_id, key=key, is_enabled=value)
            db.add(flag)
        else:
            flag.is_enabled = value

        db.commit()

        # Invalidação de Cache (Real-time propagation)
        cache_key = f"{FeatureFlagService.CACHE_PREFIX}{comp_id_str}"
        CacheService.delete(cache_key)

        logger.info(f"Feature Flag '{key}' alterada para {value} na empresa {comp_id_str}")
        return flag
