from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from accounts.api.serializers import UserDetailSerializer

from comments.api.serializers import CommentSerializer
from comments.models import Comment

from posts.models import Post

post_detail_url = HyperlinkedIdentityField(
    view_name='posts-api:detail',
    lookup_field='slug',
)

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            #'slug',
            'content',
            'publish',


        ]


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()

    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'id',
            'title',
            'slug',
            'content',
            'html',
            'publish',
            'image',
            'comments',


        ]
    def get_user(self, obj):
        return str(obj.user.username)

    def get_html(self, obj):
        return obj.get_html()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None

        return image

    def get_comments(self, obj):
        # content_type = obj.get_content_type
        # object_id = obj.id
        comment_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(comment_qs, many=True).data

        return comments

class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)

    image = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'content',
            'publish',
            'image',


        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None

        return image