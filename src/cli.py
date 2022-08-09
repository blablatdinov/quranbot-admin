"""Запуск функционала при помощи командной строки.

Functions:
    start_events_receiver
    main
"""
import asyncio
import sys

from db import database
from caching import redis_connection
from exceptions import CliError
from integrations.queue_integration import NatsEvents, NatsIntegration, NotificationCreatedEvent
from repositories.notification import NotificationRepository


async def start_events_receiver() -> None:
    """Обработка сообщений из очереди."""
    await database.connect()
    nats_integration = NatsIntegration()
    await NatsEvents([
        NotificationCreatedEvent(
            await redis_connection(),
            nats_integration,
            NotificationRepository(database),
        ),
    ]).receive()


def main() -> None:
    """Entrypoint.

    :raises CliError: cli errors
    """
    if len(sys.argv) < 2:
        raise CliError

    func = {
        'queue': start_events_receiver,
    }.get(sys.argv[1])

    if not func:
        raise CliError

    asyncio.run(func())


if __name__ == '__main__':
    main()
