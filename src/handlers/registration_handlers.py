from fastapi import APIRouter, Request

from handlers.v1.daily_content import router as daily_content_router
from handlers.v1.views.auth import router as auth_router
from handlers.v1.views.ayats import router as ayats_router
from handlers.v1.views.mailings import router as mailings_router
from handlers.v1.views.messages import router as messages_router
from fastapi.templating import Jinja2Templates
from settings import settings

router = APIRouter()
templates = Jinja2Templates(directory=settings.BASE_DIR / 'templates')

router.include_router(messages_router, prefix='/api/v1', tags=['Messages'])
router.include_router(mailings_router, prefix='/api/v1', tags=['Mailings'])
router.include_router(ayats_router, prefix='/api/v1', tags=['Ayats'])
router.include_router(daily_content_router, prefix='/api/v1', tags=['Daily content'])
router.include_router(auth_router, prefix='/api/v1', tags=['Auth'])


@router.get('/ws-ui/')
async def get_websocket_page(request: Request):
    return templates.TemplateResponse('websocket_ui.html', {'request': request})
