from django.urls import path

from blog.api.v1.views import PostsList

urlpatterns = [
    path('posts/', PostsList.as_view()),
]
