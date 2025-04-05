from django.contrib.auth import get_user_model
from django.shortcuts import render

from blog.models import Post

User = get_user_model()


def some_view(request):
    posts = Post.objects.all()
    users = User.objects.all()
    return render(request, 'blog/main.html', context={'posts': posts, 'users': users})
