from django.urls import path

from blog.views import some_view

urlpatterns = [
    path('', some_view),
]
