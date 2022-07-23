import time
from typing import Callable

import uvicorn
from asyncpg import Connection
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware

from db import QueriesCountConnection, db_connection
from handlers.registration_handlers import router
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


@app.middleware('http')
async def db_queries_count_middleware(request: Request, call_next: Callable):
    """Добавляет время обработки запроса.

    :param request: Request
    :param call_next: Callable
    :return: Response
    """
    connection = db_connection()
    request.state.connection = QueriesCountConnection(
        await connection.__anext__()
    )
    response = await call_next(request)
    response.headers['X-Queries-Count'] = str(request.state.connection.queries_count)
    await request.state.connection.close()
    return response


app.add_middleware(GZipMiddleware, minimum_size=1000)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=settings.PORT)
