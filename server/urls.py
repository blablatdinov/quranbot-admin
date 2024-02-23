"""Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView
from health_check import urls as health_urls

from server.apps.main.views import (
    AyatDetail,
    LoginView,
    ayats_page,
    index,
    landing,
    users_page,
)

admin.autodiscover()

urlpatterns = [
    # Health checks:
    path('health/', include(health_urls)),
    # Text and xml static files:
    path(
        'robots.txt',
        TemplateView.as_view(
            template_name='txt/robots.txt',
            content_type='text/plain',
        ),
    ),
    path(
        'humans.txt',
        TemplateView.as_view(
            template_name='txt/humans.txt',
            content_type='text/plain',
        ),
    ),
    # It is a good practice to have explicit index view:
    path('', landing, name='landing'),
    path('index', login_required(index), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('ayats', login_required(ayats_page), name='ayats'),
    path('ayats/<str:public_id>', login_required(AyatDetail.as_view()), name='ayat_detail'),
    path('users', login_required(users_page), name='users'),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),
        *urlpatterns,
        # Serving media files in development only:
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
