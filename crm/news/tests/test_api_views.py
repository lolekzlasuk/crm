import json
from rest_framework.test import APIClient
from django.test import TestCase, Client, override_settings
from accounts.models import UserProfile
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from ..models import KnowledgeCategory, DocumentF
from ..api.views import KnowledgeListAPIView
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


class TestKnowledgeListAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        cls.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK')
        cls.test_user3 = User.objects.create_user(
            username='testuser3', password='1X<ISRUkw+tuK')
        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)
        cls.test_user3.groups.add(newgroup)
        cls.test_category = KnowledgeCategory.objects.create(
            title='Test Category')
        cls.test_category_2 = KnowledgeCategory.objects.create(
            title='Test Category 2')

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='sal',
            location='WAW'
        )
        test_user1_userprofile.save()
        test_user2_userprofile = UserProfile.objects.create(
            user=cls.test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
        )
        test_user2_userprofile.save()
        test_user3_userprofile = UserProfile.objects.create(
            user=cls.test_user3,
            name='Test User3',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
        )
        test_user3_userprofile.save()
        cls.test_document = DocumentF.objects.create(
            title="test title",
            body='test body',
            author=cls.test_user1,
            target_location="PZN",
            target_departament="sal",
            date_created='2021-07-10T18:11:11.055162Z'
        )
        cls.factory = APIRequestFactory()

    def test_GET_if_no_permission(self):
        user = self.test_user2
        token = get_token(user)
        request = self.factory.get(
            '/news/api/knowledge/', HTTP_AUTHORIZATION='JWT ' + token)
        view = KnowledgeListAPIView.as_view()
        # force_authenticate(request, user=user,)
        # print(request)
        # client = APIClient()
        # client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # response = client.get('/news/api/knowledge/')
        response = view(request)
        # print(response.status_code)
        # response = self.client.get(reverse('news:faq'))
        self.assertEquals(response.status_code, 403)
        # self.assertRedirects(response, '/accounts/login/?next=/faq/')

    def test_GET_if_has_permission(self):
        view = KnowledgeListAPIView.as_view()
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/news/api/knowledge/', HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)
        self.assertEquals(response.status_code, 200)

    def test_view_queryset_response(self):
        user = self.test_user1
        view = KnowledgeListAPIView.as_view()
        token = get_token(user)
        request = self.factory.get(
            '/news/api/knowledge/', HTTP_AUTHORIZATION='JWT ' + token, format='json')
        response = view(request)
        # data = json.dumps(response.data)
        response.render()
        expected_respone = [{'id': 1, 'title': 'Test Category', 'docs': [], 'files': []}, {
            'id': 2, 'title': 'Test Category 2', 'docs': [], 'files': []}]
        self.assertEquals(json.loads(response.content), expected_respone)

    def test_view_queryset_filtering(self):
        user = self.test_user3
        view = KnowledgeListAPIView.as_view()
        token = get_token(user)
        request = self.factory.get(
            '/news/api/knowledge/', HTTP_AUTHORIZATION='JWT ' + token, format='json')
        response = view(request)
        # data = json.dumps(response.data)
        response.render()
        print(json.loads(response.content))
        expected_respone = [{'id': 1, 'title': 'Test Category', 'docs': [], 'files': []},
                            {'id': 2, 'title': 'Test Category 2', 'docs': [{'id': 1, 'title': 'test title', 'date_created': '2021-07-10T18:11:11.055162Z'}], 'files': []}]
        self.assertEquals(json.loads(response.content), expected_respone)

    # def test_view_if_logged_in(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('news:faq'))
    #     self.assertEqual(str(response.context['user']), 'testuser1')
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'news/docquestion_list.html')
    #
    # # def test_view_queryset_length(self):
    # #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    # #     response = self.client.get(reverse('news:faq'))
    # #     self.assertEquals(response.context['object_list'].count(),6)
    #
    # def test_view_if_files_filtered_by_category_2(self):
    #     login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
    #     response = self.client.get('%s?category=%s' % (reverse('news:faq'),2))
    #     self.assertEquals(response.context['object_list'].count(),3)
    #
    # def test_view_if_files_filtered_by_category_1(self):
    #     login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
    #     response = self.client.get('%s?category=%s' % (reverse('news:faq'),1))
    #     self.assertEquals(response.context['object_list'].count(),3)
    #
    # def test_view_if_filtered_by_location_depratament_1(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('news:faq'))
    #     self.assertEquals(response.context['object_list'].count(),8)
    #
    # def test_view_if_filtered_bylocation_depratament_2(self):
    #     login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
    #     response = self.client.get(reverse('news:faq'))
    #     self.assertEquals(response.context['object_list'].count(),6)
    #
    # def test_view_categories_queryset(self):
    #     login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
    #     response = self.client.get(reverse('news:faq'))
    #     self.assertEquals(response.context['categories'].count(),2)
