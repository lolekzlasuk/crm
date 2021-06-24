
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone
import datetime
from ..models import *
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
class NewsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFile
        fields = [
        'file',
        'miniature'
        ]


class NewsSerializer(serializers.ModelSerializer):
    files = NewsFileSerializer(many=True, read_only=True)
    class Meta:
        model = News
        fields = [
        'id',
            'body',
            'author',
            'title' ,
            'published_date',
            'files'
        ]
        read_only_fields = ['id']
class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        request = self.context.get('request')
        userprofile = request.user.userprofile
        data = data.filter(Q(target_location=userprofile.location) | Q(
            target_location="non"))
        data = data.filter(Q(target_departament=userprofile.departament) | Q(
            target_departament="non"))
        return super(FilteredListSerializer, self).to_representation(data)


class DocumentFSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = DocumentF
        fields = ['title',
                'body',
                'author',
                'date_created']


class DocFileSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = DocFile
        fields = ['file',
        'title',
        'date_created']
class KnowledgeCategorySerializer(serializers.ModelSerializer):
     docs = DocumentFSerializer(many=True, read_only=True)
     files = DocFileSerializer(many=True, read_only=True)
     class Meta:
        model = KnowledgeCategory
        fields = ['title','docs','files']


class DocQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = DocQuestion
        fields = ['id','title','body','answer','target_departament',
            'target_location',
            'category']
        read_only_fields = ['id']

class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestion
        fields = ['id','title','body','author']
        read_only_fields = ['id','author']
