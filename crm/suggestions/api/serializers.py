
from rest_framework import serializers
from django.utils import timezone
import datetime
from ..models import *
from rest_framework_jwt.settings import api_settings



class CommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super(CommentSerializer, self).to_representation(instance)
        rep['author'] = instance.author.userprofile.name
        return rep
    class Meta:
        model = Comment
        fields = [
        'id',
        'body',
        'date_created',
        'author'
        ]
read_only_fields = ['id','author','date_created']

class PostSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super(PostSerializer, self).to_representation(instance)
        rep['author'] = instance.author.userprofile.name
        rep['category'] = instance.category.title
        return rep
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = [
        'id',
        'body',
        'date_created',
        'last_activity',
        'author',
        'title',
        'category',
        'comments'
        ]
read_only_fields = ['id','author','date_created','last_activity']

class PostListSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
    total_comments = serializers.SerializerMethodField(read_only=True)
    def get_total_comments(self, Post):
        return Post.comments.count()
    def to_representation(self, instance):
        rep = super(PostListSerializer, self).to_representation(instance)
        rep['category'] = instance.category.title
        return rep
    class Meta:
        model = Post
        fields = [
        'id',
        'category',
        'title',
        'body',
        'date_created',
        'last_activity',
        'author',
        'total_comments'
        ]
    read_only_fields = ['id','author','date_created','last_activity','total_comments']

class CommentCreationSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
    class Meta:
        model = Comment
        fields = [
        'Post',
        'body',
        'author'
        ]
        read_only_fields = ['author']


class BoardCategorySerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField(read_only=True)

    def get_total_posts(self, BoardCategory):
        return BoardCategory.posts.count()
    class Meta:
        model = BoardCategory
        fields = [
        'id',
        'title',
        'total_posts'
        ]
        read_only_fields = ['total_posts','id']
