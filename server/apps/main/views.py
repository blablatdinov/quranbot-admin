"""Контроллеры."""

import datetime
import json
import time
import uuid
from dataclasses import dataclass

import attrs
import pika
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.core.cache import cache

from server.apps.main.models import Ayat, Mailing, Message, User, UserAction


def _rabbit_channel():
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
    return connection.channel()


def _publish_event(queue_name: str, event_name: str, event_version: int, event_data: dict) -> None:  # type: ignore [type-arg]
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
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps({
            'event_id': str(uuid.uuid4()),
            'event_version': event_version,
            'event_name': event_name,
            'event_time': str(int(time.time())),
            'producer': 'quranbot-admin',
            'data': event_data,
        }).encode('utf-8'),
    )


class UnreachebleCaseError(Exception):
    """Недостежимое состояние."""


def landing(request: HttpRequest) -> HttpResponse:
    """Страница с публичной информацией."""
    return render(request, 'main/landing.html')


def index(request: HttpRequest) -> HttpResponse:
    """Страница с графиками."""
    user_actions = (
        UserAction.objects.filter(date_time__date__range=['2018-01-01', datetime.datetime.now().strftime('%Y-%m-%d')])
        .values('date_time__date', 'action')
        .order_by('date_time')
    )
    data = {}
    prev_value = 0
    for row in user_actions:
        new_value = prev_value + int(row['action'] == 'Subscribed')
        data[row['date_time__date'].strftime('%Y-%m-%d')] = new_value
        prev_value = new_value
    labels = list(data.keys())
    values = list(data.values())
    return render(
        request,
        'main/index.html',
        {
            'labels': labels,
            'values': values,
        },
    )


class LoginView(View):
    """Авторизация."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Форма для входа."""
        return render(request, 'main/login.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        """Обработка данных для входа."""
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if not user:
            if not User.objects.filter(username=request.POST['username']).exists():
                return render(
                    request,
                    'main/login_form.html',
                    context={
                        'username_error': 'Пользователь не найден',
                    },
                    status=401,
                )
            else:  # not User.objects.get(username=request.POST['username']).check_password(request.POST['password']):
                return render(
                    request,
                    'main/login_form.html',
                    context={
                        'password_error': 'Пароль не верен',
                    },
                    status=401,
                )
        login(request, user)
        return redirect(reverse('ayats'))


def ayats_page(request: HttpRequest) -> HttpResponse:
    """Таблица с аятами."""
    ayats = Ayat.objects.all().order_by('ayat_id')
    paginator = Paginator(ayats, 50)
    page = paginator.page(request.GET.get('page', 1))
    if request.headers.get('Hx-Request') == 'true':
        return HttpResponse(
            '<div id="ayats-list">{0}\n{1}</div>'.format(
                render_to_string('main/ayats/ayats_list.html', {'page': page, 'target_id': 'ayats-list'}),
                render_to_string(
                    'main/pagination.html',
                    {'page': page, 'paginator': paginator, 'request': request, 'target_id': 'ayats-list'},
                ),
            ),
        )
    return render(
        request,
        'main/ayats/ayats.html',
        context={
            'page': page,
            'paginator': paginator,
            'target_id': 'ayats-list',
        },
    )


class AyatDetail(View):
    """Детальная информация об аяте."""

    def get(self, request: HttpRequest, public_id: uuid.UUID) -> HttpResponse:
        """Детальная информация об аяте."""
        ayat = Ayat.objects.get(public_id=public_id)
        return render(request, 'main/ayats/ayat_detail.html', context={'ayat': ayat})

    def post(self, request: HttpRequest, public_id: uuid.UUID) -> HttpResponse:
        """Обновить аят."""
        ayat = Ayat.objects.get(public_id=public_id)
        return render(request, 'main/ayats/ayat_detail_form.html', context={'ayat': ayat})


def users_page(request: HttpRequest) -> HttpResponse:
    """Страница со списком пользователей."""
    users = User.objects.all()
    if request.GET.get('is_active'):
        users = users.filter(is_active=request.GET.get('is_active') == 'true')
    users = users.order_by(request.GET.get('order', '-date_joined'), 'chat_id')
    paginator = Paginator(users, 50)
    page = paginator.page(request.GET.get('page', 1))
    match request.headers.get('Hx-Request'):
        case 'true':
            template = 'main/users_content.html'
        case _:
            template = 'main/users_page.html'
    return render(
        request,
        template,
        context={
            'page': page,
            'paginator': paginator,
            'is_active': request.GET.get('is_active'),
            'url': reverse('users'),
            'target_id': '#users-list',
        },
    )


def days(request: HttpRequest) -> HttpResponse:
    """Получить/обновить дни для аятов."""
    template = 'main/days.html'
    if request.method == 'POST':
        day = int(request.POST['day'])
        ayats = Ayat.objects.filter(
            ayat_id__in=[item_name[5:] for item_name in request.POST if item_name.startswith('ayat')],
        )
        ayats.update(day=day)
        template = 'main/days_form.html'
        for ayat in ayats:
            _publish_event(
                'quranbot.ayats',
                'Ayat.Changed',
                1,
                {
                    'public_id': str(ayat.public_id),
                    'day': day,
                    'audio_id': str(ayat.audio_id),
                    'ayat_number': ayat.ayat_number,
                    'content': ayat.content,
                    'arab_text': ayat.arab_text,
                    'transliteration': ayat.transliteration,
                },
            )
    last_ayat_day = Ayat.objects.filter(day__isnull=False).latest('day').day
    if not last_ayat_day:  # pragma: no cover
        msg = 'unreacheble'
        raise UnreachebleCaseError(msg)
    next_day = last_ayat_day + 1
    return render(
        request,
        template,
        context={
            'next_day': next_day,
            'ayats_without_day': Ayat.objects.filter(day__isnull=True).order_by('ayat_id'),
        },
    )


def messages(request: HttpRequest) -> HttpResponse:
    """Страница со списком сообщений."""
    messages = Message.objects.all()
    messages = messages.order_by('-message_id')
    paginator = Paginator(messages, 50)
    page = paginator.page(request.GET.get('page', 1))
    match request.headers.get('Hx-Request'):
        case 'true':
            template = 'main/messages_content.html'
        case _:
            template = 'main/messages_page.html'
    return render(
        request,
        template,
        context={
            'page': page,
            'paginator': paginator,
            'url': reverse('messages'),
            'target_id': '#messages-list',
        },
    )


def message(request: HttpRequest, message_id: int) -> HttpResponse:
    """Просмотр сообщения."""
    message = Message.objects.get(message_id=int(message_id))
    trigger_message_json = None
    trigger_message = None
    if message.trigger_message_id:
        trigger_message = Message.objects.filter(message_id=message.trigger_message_id).first()
        if trigger_message:
            trigger_message_json = json.dumps(trigger_message.message_json, indent=2, ensure_ascii=False)
    return render(
        request,
        'main/message_detail.html',
        context={
            'message': message,
            'trigger_message': trigger_message,
            'trigger_message_json': trigger_message_json,
            'message_json': json.dumps(message.message_json, indent=2, ensure_ascii=False),
        },
    )


def users_count_badge(request: HttpRequest) -> HttpResponse:
    """Кол-во пользователей."""
    return JsonResponse({
        'schemaVersion': 1,
        'label': 'users count',
        'message': str(User.objects.count()),
        'color': 'informational',
    })


class MailingsView(View):
    """Контроллер для рассылок."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """Создание рассылки."""
        _publish_event(
            'quranbot.mailings',
            'Mailing.Created',
            1,
            {
                'text': request.POST['text'],
                'group': request.POST['group'],
            },
        )
        paginator = Paginator(Mailing.objects.all(), 50)
        page = paginator.page(request.GET.get('page', 1))
        return render(
            request,
            'main/mailings_content.html',
            context={
                'page': page,
                'paginator': paginator,
                'target_id': '#mailings-list',
            },
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        """Получить список рассылок."""
        paginator = Paginator(Mailing.objects.all(), 50)
        page = paginator.page(request.GET.get('page', 1))
        return render(
            request,
            'main/mailings_page.html',
            context={
                'page': page,
                'paginator': paginator,
                'target_id': '#mailings-list',
            },
        )


def new_mailing(request: HttpRequest) -> HttpResponse:
    """Форма для создания рассылки."""
    if 'Hx-Request' in request.headers:
        return render(request, 'main/new_mailing_form.html')
    return render(request, 'main/new_mailing_page.html')


@attrs.define(frozen=True)
class FailedEvent:

    _json: dict

    @property
    def event_name(self):
        return self._json['event_name']

    @property
    def event_version(self):
        return self._json['event_version']

    @property
    def event_time(self):
        return self._json['event_time']

    @property
    def event_id(self):
        return self._json['event_id']

    @property
    def json(self):
        return json.dumps(self._json, indent=2, ensure_ascii=False)


def failed_events(request: HttpRequest) -> HttpResponse:
    channel = _rabbit_channel()
    events = []
    body = 1
    while body:
        method_frame, _, body = channel.basic_get('failed-events')
        if not body:
            break
        events.append(
            (
                method_frame,
                FailedEvent(json.loads(body.decode('utf-8'))),
            )
        )
    bodies = []
    for method_frame, body in events:
        bodies.append(body)
        channel.basic_nack(method_frame.delivery_tag)
    cache.set('failed_events', '[{0}]'.format(','.join([body.json for body in bodies])))
    return render(request, 'main/failed_events.html', context={
        'bodies': bodies,
    })


def resolve_event(request: HttpRequest, event_id: str) -> HttpResponse:
    channel = _rabbit_channel()
    body = 1
    bodies = [
        FailedEvent(x)
        for x in json.loads(cache.get('failed_events'))
        if x['event_id'] != event_id
    ]
    frames = []
    while body:
        method_frame, _, body = channel.basic_get('failed-events')
        if not body:
            break
        if json.loads(body.decode('utf-8'))['event_id'] == event_id:
            channel.basic_ack(method_frame.delivery_tag)
        else:
            frames.append(method_frame)
    for method_frame in frames:
        channel.basic_nack(method_frame.delivery_tag)
    cache.set('failed_events', '[{0}]'.format(','.join([body.json for body in bodies])))
    return render(request, 'main/failed_events_table.html', context={
        'bodies': bodies,
    })
