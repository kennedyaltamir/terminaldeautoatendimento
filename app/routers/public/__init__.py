
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 12:30:00

from fastapi import APIRouter
from app.routers.public.menu import router as menu_router
from app.routers.public.tables import router as tables_router
from app.routers.public.orders import router as orders_router # NOVO

router = APIRouter()

# Agrega as rotas públicas
router.include_router(menu_router)
router.include_router(tables_router)
router.include_router(orders_router) # NOVO

