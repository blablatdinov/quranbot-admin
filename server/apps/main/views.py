"""Контроллеры."""

import json
import uuid

import pika
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from server.apps.main.models import Ayat, Message, User


class UnreachebleCaseError(Exception):
    """Недостежимое состояние."""


def landing(request: HttpRequest) -> HttpResponse:
    """Страница с публичной информацией."""
    return render(request, 'main/landing.html')


def index(request: HttpRequest) -> HttpResponse:
    """Страница с графиками."""
    data = {'2022-01-01': 10, '2022-01-02': 20, '2022-01-03': 30, '2022-01-04': 25, '2022-01-05': 40}
    # Преобразуем данные в списки для labels (даты) и data (значения)
    labels = list(data.keys())
    values = list(data.values())
    return render(request, 'main/index.html', {'labels': labels, 'values': values})


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
    users = users.order_by(request.GET.get('order', 'date_joined'), 'chat_id')
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
        for ayat in ayats:
            channel.basic_publish(
                exchange='',
                routing_key='quranbot_queue',
                body=json.dumps({
                    'event_id': str(uuid.uuid4()),
                    'event_version': 1,
                    'event_name': 'Ayat.Changed',
                    'event_time': '392409283',
                    'producer': 'quranbot-admin',
                    'data': {
                        'public_id': str(ayat.public_id),
                        'day': day,
                        'audio_id': str(ayat.audio_id),
                        'ayat_number': ayat.ayat_number,
                        'content': ayat.content,
                        'arab_text': ayat.arab_text,
                        'transliteration': ayat.transliteration,
                    },
                }).encode('utf-8'),
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


def users_count_badge(request: HttpRequest) -> HttpResponse:
    """Кол-во пользователей."""
    return JsonResponse({
        'schemaVersion': 1,
        'label': 'users count',
        'message': str(User.objects.count()),
        'color': 'informational',
    })
