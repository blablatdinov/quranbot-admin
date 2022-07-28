from typing import Optional

from fastapi import WebSocket, Header, Depends

from services.auth import User


class WebsocketStorage(object):

    _storage = []

    def add(self, new: WebSocket):
        self._storage.append(new)

    def to_list(self):
        return self._storage


websocket_storage = WebsocketStorage()


async def websocket_endpoint(
    websocket: WebSocket,
    # token: str = Header('', alias='Authorization')
):
    # user = User.get_from_token(token)
    # print(user)
    await websocket.accept()
    websocket_storage.add(websocket)
    while True:
        data = await websocket.receive_text()
        for client in websocket_storage.to_list():
            await client.send_text(f"Message text was: {data}")
