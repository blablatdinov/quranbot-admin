"""Точка входа в приложение.

Functions:
    add_process_time_header: TODO move it into middlewares module
    startup
"""
import time
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware

from db import database
from handlers.registration_handlers import router
from logging_settings import configure_logging

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


@app.on_event('startup')
async def startup():
    """Действия, при запуске приложения."""
    await database.connect()


app.add_middleware(GZipMiddleware, minimum_size=1000)
configure_logging()
