
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone
import datetime
from ..models import *
from rest_framework_jwt.settings import api_settings
from django.db.models import Q

def sizify(value):
    """
    Simple kb/mb/gb size snippet for templates:

    {{ product.file.size|sizify }}
    """
    #value = ing(value)
    if value < 512000:
        value = value / 1024.0
        ext = 'kb'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'mb'
    else:
        value = value / 1073741824.0
        ext = 'gb'
    return '%s %s' % (str(round(value, 2)), ext)

class NewsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFile
        fields = [
        'file',
        'miniature'
        ]




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
    author = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
    def to_representation(self, instance):
        rep = super(DocumentFSerializer, self).to_representation(instance)
        rep['author'] = instance.author.userprofile.name
        return rep
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = DocumentF
        fields = ['id',
                'title',
                'body',
                'author',
                'date_created']
        read_only_fields = ['id','author','date_created']

class DocFileSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super(DocFileSerializer, self).to_representation(instance)
        rep['size'] = sizify(instance.file.size)
        return rep
    size = serializers.CharField(source='file.size', read_only=True)
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = DocFile
        fields = ['id',
                'title',
                'file',
                'size',
                'date_created']

        read_only_fields = ['id','size','date_created']
class KnowledgeCategorySerializer(serializers.ModelSerializer):
     docs = DocumentFSerializer(many=True, read_only=True)
     files = DocFileSerializer(many=True, read_only=True)
     class Meta:
        model = KnowledgeCategory
        fields = ['id','title','docs','files']


class DocQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = DocQuestion
        fields = ['id','title','body','answer','target_departament',
            'target_location',
            'category']
        read_only_fields = ['id']

class UserQuestionSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
    class Meta:
        model = UserQuestion
        fields = ['id','title','body','author']
        read_only_fields = ['id','author']


class DocFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocFile
        fields = [
        'file',
        'title',
        'target_departament',
        'target_location',
        'category',
        ]



class NewsListSerializer(serializers.ModelSerializer):

    files = NewsFileSerializer(many=True, read_only=True)
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = News
        fields = [
        'id',
            'title' ,
            'published_date',
            'files'
        ]
        read_only_fields = ['id']

class NewsCRUDSerializer(serializers.ModelSerializer):

    files = NewsFileSerializer(many=True, read_only=True)
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = News
        fields = [
        'id',
        'body',
        'author',
        'title',
        'files',
        'target_departament',
        'target_location',

        ]
        read_only_fields = ['id','author']
