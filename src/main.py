import time
from typing import Callable

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware

from handlers.registration_handlers import router
from logging_settings import configure_logging
from settings import settings

app = FastAPI()

app.include_router(router)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next: Callable):
    """Добавляет время обработки запроса.

    :param request: Request
    :param call_next: Callable
    :return: Response
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = '{0} s'.format(str(process_time))
    return response


#app.add_middleware(GZipMiddleware, minimum_size=1000)

if __name__ == '__main__':
    uvicorn.run('main:app', port=settings.PORT, workers=10)
