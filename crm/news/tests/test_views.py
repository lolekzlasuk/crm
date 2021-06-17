from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
from datetime import date, timedelta
from news import models
from django.contrib.auth.models import Permission

class TestKnowledgeCategoryListView(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')

        test_user1.save()
        test_user2.save()


        test_user2.group.add(name="test_permissions_group")
        test_user2.save()



    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:knowledge'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/news/knowledge')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:knowledge'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendary/knowledgecategory_lists.html')
