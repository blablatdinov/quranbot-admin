from fastapi import APIRouter

from handlers.v1.mailings import router as mailings_router
from handlers.v1.messages import router as messages_router

router = APIRouter()

router.include_router(messages_router, prefix='/api/v1', tags=['Messages'])
router.include_router(mailings_router, prefix='/api/v1', tags=['Mailings'])
