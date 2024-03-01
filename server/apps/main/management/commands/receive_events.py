import pika
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(
            pika.URLParameters(
                'amqp://{0}:{1}@{2}:5672/{3}'.format(
                    settings.RABBITMQ_USER,
                    settings.RABBITMQ_PASS,
                    settings.RABBITMQ_HOST,
                    settings.RABBITMQ_VHOST,
                ),
            ),
        )
        channel = connection.channel()
        channel.queue_declare(queue='quranbot_queue')
        for method_frame, properties, body in channel.consume('quranbot_queue'):
            print(method_frame)
            print(properties)
            print(body)
            channel.basic_ack(method_frame.delivery_tag)
