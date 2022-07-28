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
from integrations.client import HttpClient
from integrations.event_handlers.message_created import MessageCreatedEvent
from integrations.event_handlers.notification_created import NotificationCreatedEvent
from integrations.event_handlers.user_subscribed import UserSubscribedEvent
from integrations.queue_integration import NatsEvents, NatsIntegration
from integrations.umma import AbsolutedSuraPages, FilteredSuraPages, SuraPages
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
            MessageRepository(database),
        ),
        UserSubscribedEvent(
            UserRepository(database),
            UserActionRepository(database),
        ),
    ]).receive()


class QuranParser(object):

    def __init__(self, sura_links: SuraPagesInterface):
        self._sura_links = sura_links

    async def run(self):
        links = await self._sura_links.get_links()
        print(links)


class Main(object):

    def main(self):
        parser = QuranParser(
            AbsolutedSuraPages(
                FilteredSuraPages(
                    SuraPages(
                        HttpClient('https://umma.ru/perevod-korana/'),
                    ),
                ),
            )
        ).run()
        asyncio.run(parser)


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
