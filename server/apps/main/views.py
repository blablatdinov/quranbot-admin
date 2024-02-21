"""Контроллеры."""

import uuid

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from server.apps.main.models import Ayat, User


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
            username_error = None
            password_error = None
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
                render_to_string('main/ayats_list.html', {'page': page}),
                render_to_string('main/pagination.html', {'page': page, 'paginator': paginator}),
            ),
        )
    return render(
        request,
        'main/ayats.html',
        context={
            'page': page,
            'paginator': paginator,
        },
    )


class AyatDetail(View):
    """Детальная информация об аяте."""

    def get(self, request: HttpRequest, public_id: uuid.UUID) -> HttpResponse:
        """Детальная информация об аяте."""
        ayat = Ayat.objects.get(public_id=public_id)
        return render(request, 'main/ayat_detail.html', context={'ayat': ayat})

    def post(self, request: HttpRequest, public_id: uuid.UUID) -> HttpResponse:
        """Обновить аят."""
        ayat = Ayat.objects.get(public_id=public_id)
        return render(request, 'main/ayat_detail_form.html', context={'ayat': ayat})
