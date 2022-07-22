from fastapi import APIRouter

from handlers.v1.messages import router as messages_router

router = APIRouter()

router.include_router(messages_router, prefix='/api/v1')
