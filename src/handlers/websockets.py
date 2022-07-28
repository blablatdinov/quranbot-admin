from fastapi import WebSocket, Query
from pydantic import BaseModel

from repositories.auth import UserSchema
from services.auth import User


class WebsocketStorageItem(BaseModel):

    user: UserSchema
    websocet: WebSocket


class WebsocketStorage(object):

    _storage: list[WebsocketStorageItem] = []

    def add(self, new: WebsocketStorageItem):
        self._storage.append(new)

    def to_list(self):
        return self._storage


websocket_storage = WebsocketStorage()


async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    user = User.get_from_token(token)
    print(websocket.scope)
    await websocket.accept()
    websocket_storage.add(
        WebsocketStorageItem(
            user=user,
            websocket=websocket,
        )
    )
    while True:
        data = await websocket.receive_text()
        for client in websocket_storage.to_list():
            await client.send_text(f"Message text was: {data}")
