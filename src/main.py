import uvicorn
from fastapi import FastAPI

from handlers.registration_handlers import router
from settings import settings

app = FastAPI()

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=settings.PORT)
