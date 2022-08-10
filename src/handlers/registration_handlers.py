"""Регистрация обработчиков HTTP запросов.

Functions:
    get_websocket_page

Misc variables:
    router
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from handlers.v1.daily_content import router as daily_content_router
from handlers.v1.views.auth import router as auth_router
from handlers.v1.views.ayats import router as ayats_router
from handlers.v1.views.debug import router as debug_router
from handlers.v1.views.files import router as files_router
from handlers.v1.views.mailings import router as mailings_router
from handlers.v1.views.messages import router as messages_router
from handlers.v1.views.notification import router as notification_router
from handlers.v1.views.users import router as users_router
from settings import settings

templates = Jinja2Templates(directory=settings.BASE_DIR / 'templates')
router = APIRouter(prefix='/api/v1', tags=['v1'])

router.include_router(messages_router, tags=['Messages'])
router.include_router(mailings_router, tags=['Mailings'])
router.include_router(ayats_router, tags=['Ayats'])
router.include_router(daily_content_router, tags=['Daily content'])
router.include_router(auth_router, tags=['Auth'])
router.include_router(notification_router, tags=['Notifications'])
router.include_router(users_router, tags=['Users'])
router.include_router(files_router, tags=['Files'])

if settings.DEBUG:
    router.include_router(debug_router, tags=['Debug'])


@router.get('/ws-ui/')
async def get_websocket_page(request: Request):
    """Страница для проверки websocket'ов.

    :param request: Request
    :return: templates.TemplateResponse
    """
    return templates.TemplateResponse('websocket_ui.html', {'request': request})
