import datetime
from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def build_url(request: HttpRequest, order_param: str, filter_param):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def add_page_param(request: HttpRequest, page: int):
    params = {key: value for key, value in request.GET.items()}
    params['page'] = page
    return '{0}?{1}'.format(
        request.path,
        '&'.join([f'{key}={value}' for key, value in params.items()])
    )


@register.simple_tag
def add_filter_param(request: HttpRequest, name: str, value: str):
    params = {key: value for key, value in request.GET.items()}
    params[name] = value
    return '{0}?{1}'.format(
        request.path,
        '&'.join([f'{key}={value}' for key, value in params.items()])
    )


@register.simple_tag
def add_sorting_param(request: HttpRequest, value: str):
    params = {key: value for key, value in request.GET.items()}
    if params.get('order'):
        if params['order'].startswith('-'):
            params['order'] = params['order'][1:]
        else:
            params['order'] = '-' + params['order']
    else:
        params['order'] = value
    return '{0}?{1}'.format(
        request.path,
        '&'.join([f'{key}={value}' for key, value in params.items()])
    )
