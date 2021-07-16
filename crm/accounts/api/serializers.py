
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone
import datetime
from accounts.models import UserProfile
from rest_framework_jwt.settings import api_settings
expire_delta             = api_settings.JWT_REFRESH_EXPIRATION_DELTA


jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(style={'input_type': 'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    # token_response = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [

        'username',
        'email',
        'password',
        'password2',
        'token',
        'expires',
        'message'
        ]
        extra_kwargs = {'password': {'write_only':True}}

    def get_message(self, obj):
        return "user registered"
    # def get_token_response(self,obj):
    #     user = obj
    #     payload = jwt_payload_handler(user)
    #     token = jwt_encode_handler(payload)
    #     context = self.context
    #     request = context['request']
    #     print(request.user.is_authenticated)
    #     response = jwt_response_payload_handler(token, user, request=context['request'])
    #     return response





    def validate_email(self,value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("user with that email already exists")
        return value

    def validate_username(self,value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("user with that username already exists")
        return value

    def get_token(self,obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def get_expires(self,obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate(self,data):
        pw = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        # print(validated_data)
        user_obj = User(
                username = validated_data.get('username'),
                email = validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))

        user_obj.save()
        return user_obj


class ChangePasswordSerializer(serializers.Serializer):

    model = User
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def get_message(self, obj):
        return "Password has been changed"


    def validate(self,data):

        pw = data.get('new_password')
        pw2 = data.get('new_password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data
    #
    # def validate_current_password(self,data,obj):
    #     user = obj
    #     current_pw = data.get('current_password')
    #     if current_pw != user.password:
    #         raise serializers.ValidationError("Current password must match")
    #     print("old pw correct")
    #     return data


        # user_obj.set_password(validated_data.get('password'))


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
        'profile_pic',
        'name',
        'telephone',
        'email',
        'position',
        'departament',
        'location',
        ]
        read_only_fields = ['name',
                'telephone',
                'email',
                'position',
                'departament',
                ]
