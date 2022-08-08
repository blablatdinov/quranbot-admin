from pydantic import BaseModel


class NotificationCreateModel(BaseModel):

    text: str
