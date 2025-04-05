from rest_framework import generics

from blog.api.v1.serializers import PostSerializer
from blog.models import Post


class PostsList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
