from django.contrib.auth.backends import ModelBackend, UserModel
from .models import UserProfile
from django.db.models import Q
from django.contrib.auth.models import User


class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        try:
            userprofile = UserProfile.objects.get(Q(email__iexact=username) | Q(
                telephone__iexact=username) | Q(user__username__iexact=username))
            user = userprofile.user
        except UserProfile.DoesNotExist:
            user = UserModel.objects.get(username=username)

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user
