"""Обработчики HTTP запросов связанных с уведомлениями.

Functions:
    create_notification
    mark_notification_readed
"""
import uuid

from fastapi import APIRouter, Depends, status

from handlers.v1.schemas.notifications import NotificationCreateModel, NotificationResponseSchema
from integrations.queue_integration import NatsIntegration
from repositories.notification import NotificationInsertQueryResult, NotificationRepository
from services.auth import User

router = APIRouter(prefix='/notifications')


@router.get('/', response_model=list[NotificationResponseSchema])
async def get_notifications(
    notification_repository: NotificationRepository = Depends(),
    _: User = Depends(User.get_from_token),
) -> list[NotificationResponseSchema]:
    """Получить уведомления.

    :param notification_repository: NotificationRepository
    :return: list[NotificationResponseSchema]
    """
    return await notification_repository.get_notifications()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=NotificationInsertQueryResult)
async def create_notification(
    input_data: NotificationCreateModel,
    nats_integration: NatsIntegration = Depends(),
    notification_repository: NotificationRepository = Depends(),
    _: User = Depends(User.get_from_token),
) -> NotificationInsertQueryResult:
    """Создать уведомление.

    :param input_data: NotificationCreateModel
    :param nats_integration: NatsIntegration
    :param notification_repository: NotificationRepository
    :return: NotificationInsertQueryResult
    """
    notification_uuid = uuid.uuid4()
    await nats_integration.send(
        {'public_id': str(notification_uuid), 'text': input_data.text}, 'Notification.Created', 1,
    )
    return NotificationInsertQueryResult(uuid=notification_uuid, text=input_data.text)


@router.patch('/{notification_uuid}/mark-readed/', status_code=status.HTTP_201_CREATED)
async def mark_notification_readed(
    notification_uuid: uuid.UUID,
    notification_repository: NotificationRepository = Depends(),
    _: User = Depends(User.get_from_token),
):
    """Пометить уведомление прочитанным.

    :param notification_uuid: uuid.UUID
    :param notification_repository: NotificationRepository
    """
    await notification_repository.mark_as_readed(notification_uuid)
