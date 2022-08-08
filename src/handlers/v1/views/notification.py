from fastapi import APIRouter, Depends, status

from handlers.v1.schemas.notifications import NotificationCreateModel
from integrations.queue_integration import NatsIntegration

router = APIRouter()


@router.post('/notification/', status_code=status.HTTP_201_CREATED)
async def create_notification(input_data: NotificationCreateModel, nats_integration: NatsIntegration = Depends()):
    await nats_integration.send(input_data.dict(), 'Notification.Created', 1)
