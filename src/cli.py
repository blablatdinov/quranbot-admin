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
from integrations.client import HttpClient
from integrations.umma import SuraPages, FilteredSuraPages, SuraPagesInterface, AbsolutedSuraPages
from integrations.client import ClientRequest
from integrations.umma import (
    AbsolutedSuraPages,
    FilteredSuraPages,
    RequestListFromUrls,
    SuraPages,
    SuraPagesHTML, PreloadedStateStrings, TrimmedPreloadedStateString,
)


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

    def __init__(self, data):
        self._data = data

    async def run(self):
        res = self._data.find()
        async for x in res:
            print(x)


class Main(object):

    def main(self):
        parser = QuranParser(
            TrimmedPreloadedStateString(
                PreloadedStateStrings(
                    SuraPagesHTML(
                        RequestListFromUrls(
                            AbsolutedSuraPages(
                                FilteredSuraPages(
                                    SuraPages(
                                        ClientRequest.new().url('https://umma.ru/perevod-korana/'),
                                    ),
                                ),
                            ),
                        )
                    )
                )
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
