import asyncio
import sys

from integrations.queue_integration import NatsEvents, NotificationCreatedEvent, NatsIntegration
from caching import redis_connection


async def start_events_receiver():
    nats_integration = NatsIntegration()
    await NatsEvents([
        NotificationCreatedEvent(
            await redis_connection(),
            nats_integration,
        ),
    ]).receive()


def main():
    """Entrypoint.

    :raises BaseAppError: cli errors
    """
    if len(sys.argv) < 2:
        raise BaseAppError

    func = {
        'queue': start_events_receiver,
    }.get(sys.argv[1])

    if not func:
        raise BaseAppError

    asyncio.run(func())


if __name__ == '__main__':
    main()
