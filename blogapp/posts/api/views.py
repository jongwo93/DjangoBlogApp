from rest_framework.generics import (
                                    CreateAPIView,
                                    ListAPIView,
                                    RetrieveAPIView,
                                    UpdateAPIView,
                                    DestroyAPIView,
                                    )

from posts.models import Post

from .serializers import (
                        PostCreateUpdateSerializer,
                        PostListSerializer,
                        PostDetailSerializer,
                        )


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    # lookup_url_kwarg = 'abc'


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abc'

class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abc'

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abc'



class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


