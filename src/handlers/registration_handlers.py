from fastapi import APIRouter

from handlers.v1.ayats import router as ayats_router
from handlers.v1.mailings import router as mailings_router
from handlers.v1.messages import router as messages_router
from handlers.v1.daily_content import router as daily_content_router

router = APIRouter()

router.include_router(messages_router, prefix='/api/v1', tags=['Messages'])
router.include_router(mailings_router, prefix='/api/v1', tags=['Mailings'])
router.include_router(ayats_router, prefix='/api/v1', tags=['Ayats'])
router.include_router(daily_content_router, prefix='/api/v1', tags=['Daily content'])
