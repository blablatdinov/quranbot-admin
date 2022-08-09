from fastapi import APIRouter, Depends, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

from integrations.queue_integration import NatsIntegration


router = APIRouter()


class EventInputData(BaseModel):
    
    name: str
    version: int
    data: dict


@router.post('/')
async def create_event(
    event_input_data: EventInputData,
    nats_integration: NatsIntegration = Depends(),
):
    try:
        await nats_integration.send(
            event_input_data.data,
            event_input_data.name,
            event_input_data.version,
        )
    except TypeError as exc: 
        return PlainTextResponse(content=str(exc), status_code=422)
