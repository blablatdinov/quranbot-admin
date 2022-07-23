from fastapi import APIRouter

from handlers.v1.views.ayats import router as ayats_router
from handlers.v1.views.mailings import router as mailings_router
from handlers.v1.views.messages import router as messages_router

router = APIRouter()

router.include_router(messages_router, prefix='/api/v1', tags=['Messages'])
router.include_router(mailings_router, prefix='/api/v1', tags=['Mailings'])
router.include_router(ayats_router, prefix='/api/v1', tags=['Ayats'])
