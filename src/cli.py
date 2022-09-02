"""Запуск функционала при помощи командной строки.

Functions:
    start_events_receiver
    main
"""
import asyncio
import sys

from caching import redis_connection
from db.connection import database
from exceptions import CliError
from integrations.queue_integration import NatsEvents, NatsIntegration, NotificationCreatedEvent, MessageCreatedEvent, UserSubscribedEvent
from repositories.auth import UserRepository
from repositories.messages import MessageRepository
from repositories.notification import NotificationRepository
from repositories.user_action import UserActionRepository


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
        MessageCreatedEvent(
            nats_integration,
            MessageRepository(database),
        ),
        UserSubscribedEvent(
            nats_integration,
            UserRepository(database),
            UserActionRepository(database),
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
