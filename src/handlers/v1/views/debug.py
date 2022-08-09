"""Модуль, содержащий ручки для отладки.

Classes:
    EventInputData

Functions:
    create_event
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from integrations.queue_integration import NatsIntegration

router = APIRouter()


class EventInputData(BaseModel):
    """Схема для создания событий в очереди через API."""

    name: str
    version: int
    event_data: dict


@router.post('/')
async def create_event(
    event_input_data: EventInputData,
    nats_integration: NatsIntegration = Depends(),
) -> PlainTextResponse:
    """Создание события.

    :param event_input_data: EventInputData
    :param nats_integration: NatsIntegration
    :return: PlainTextResponse
    """
    try:
        await nats_integration.send(
            event_input_data.event_data,
            event_input_data.name,
            event_input_data.version,
        )
    except TypeError as exc:
        return PlainTextResponse(content=str(exc), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return PlainTextResponse(status_code=status.HTTP_200_OK)
