"""Тэги для составления адресов."""

from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def add_page_param(request: HttpRequest, page: int) -> str:
    """Добавить/изменить параметр пагинации."""
    params = dict(request.GET)
    params['page'] = str(page)
    return '{0}?{1}'.format(request.path, '&'.join([f'{key}={value}' for key, value in params.items()]))


@register.simple_tag
def add_filter_param(request: HttpRequest, name: str, value: str) -> str:
    """Добавить/изменить параметр фильтрации."""
    params = dict(request.GET)
    params[name] = value
    return '{0}?{1}'.format(request.path, '&'.join([f'{key}={value}' for key, value in params.items()]))


@register.simple_tag
def add_sorting_param(request: HttpRequest, value: str) -> str:
    """Добавить/изменить параметр сортировки."""
    params = dict(request.GET)
    order_param = params.get('order', [None])[0]
    if order_param:
        if order_param.startswith('-'):
            params['order'] = order_param[1:]
        else:
            params['order'] = '-' + order_param
    else:
        params['order'] = value
    return '{0}?{1}'.format(request.path, '&'.join([f'{key}={value}' for key, value in params.items()]))
