"""Обработчики HTTP запросов связанных с уведомлениями.

Functions:
    create_notification
"""
from fastapi import APIRouter, Depends, status

from handlers.v1.schemas.notifications import NotificationCreateModel
from integrations.queue_integration import NatsIntegration
from services.auth import User

router = APIRouter()


@router.post('/notification/', status_code=status.HTTP_201_CREATED)
async def create_notification(
    input_data: NotificationCreateModel,
    nats_integration: NatsIntegration = Depends(),
    _: User = Depends(User.get_from_token),
):
    """Создать уведомление.

    :param input_data: NotificationCreateModel
    :param nats_integration: NatsIntegration
    """
    await nats_integration.send(input_data.dict(), 'Notification.Created', 1)
