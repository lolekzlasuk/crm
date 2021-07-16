from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User, Permission, Group
from django.utils import timezone
import json
from datetime import date, timedelta
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework_jwt.settings import api_settings
from accounts.models import UserProfile
from ..models import KnowledgeCategory, DocumentF, DocQuestion, DocFile, \
    NewsFile, DocumentF, News, NotificationReadFlag
from ..api.views import KnowledgeListAPIView, DocQuestionListAPIView, \
    UserQuestionCreateAPIView, DocFileCreateAPIView, NewsFileCreateAPIView, \
    DocumentFViewSet, NewsViewSet


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

        response = view(request)

        self.assertEquals(response.status_code, 403)

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

        response.render()

        expected_respone = [{'id': 1, 'title': 'Test Category', 'docs': [], 'files': []},
                            {'id': 2, 'title': 'Test Category 2', 'docs': [{'id': 1, 'title': 'test title', 'date_created': '2021-07-10T18:11:11.055162Z'}], 'files': []}]
        self.assertEquals(json.loads(response.content), expected_respone)


class TestDocQuestionListAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        cls.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK')
        cls.test_user3 = User.objects.create_user(
            username='testuser3', password='1X<ISRUkw+tuK')
        newgroup = Group.objects.create(name='Managers')
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

        cls.test_question = DocQuestion.objects.create(
            title="test title",
            body='test body',
            author=cls.test_user1,
            answer="test answer",
            category=cls.test_category,
        )
        cls.test_question2 = DocQuestion.objects.create(
            title="test title2",
            body='test body2',
            author=cls.test_user1,
            answer="test answer2",
            category=cls.test_category,
            target_location="PZN",
            target_departament="sal",
        )
        cls.factory = APIRequestFactory()

    def test_GET_if_no_permission(self):
        user = self.test_user2
        token = get_token(user)
        request = self.factory.get(
            '/news/api/faq/', HTTP_AUTHORIZATION='JWT ' + token)
        view = DocQuestionListAPIView.as_view()
        response = view(request)
        self.assertEquals(response.status_code, 403)

    def test_GET_if_has_permission(self):
        view = DocQuestionListAPIView.as_view()
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/news/api/faq/', HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)
        self.assertEquals(response.status_code, 200)

    def test_view_queryset_response(self):
        user = self.test_user1
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)
        request = self.factory.get(
            '/news/api/faq/', HTTP_AUTHORIZATION='JWT ' + token, format='json')
        response = view(request)

        response.render()

        expected_respone = [{'id': 1, 'title': 'test title', 'body': 'test body', 'answer': 'test answer',
                             'target_departament': 'non', 'target_location': 'non', 'category': 1}]
        self.assertEquals(json.loads(response.content), expected_respone)

    def test_view_queryset_search(self):
        user = self.test_user3
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)
        request = self.factory.get(
            '/news/api/faq/?q=title2', HTTP_AUTHORIZATION='JWT ' + token, format='json')
        response = view(request)

        response.render()

        expected_respone = [{'id': 2, 'title': 'test title2', 'body': 'test body2', 'answer': 'test answer2',
                             'target_departament': 'sal', 'target_location': 'PZN', 'category': 1}]
        self.assertEquals(json.loads(response.content), expected_respone)

    def test_view_queryset_filtering(self):
        user = self.test_user1
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)
        request = self.factory.get(
            '/news/api/faq/', HTTP_AUTHORIZATION='JWT ' + token, format='json')
        response = view(request)

        response.render()

        expected_respone = [{'id': 1, 'title': 'test title', 'body': 'test body', 'answer': 'test answer',
                             'target_departament': 'non', 'target_location': 'non', 'category': 1}]
        self.assertEquals(json.loads(response.content), expected_respone)
        user3 = self.test_user3
        token = get_token(user3)
        request = self.factory.get(
            '/news/api/faq/', HTTP_AUTHORIZATION='JWT ' + token, format='json')
        response = view(request)
        response.render()

        expected_respone = [{'id': 2, 'title': 'test title2', 'body': 'test body2', 'answer': 'test answer2', 'target_departament': 'sal', 'target_location':
                             'PZN', 'category': 1}, {'id': 1, 'title': 'test title', 'body': 'test body', 'answer': 'test answer',
                                                     'target_departament': 'non', 'target_location': 'non', 'category': 1}]
        self.assertEquals(json.loads(response.content), expected_respone)

    def test_view_object_creation(self):
        user = self.test_user1
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)
        data = {
            'title': "test title",
            'body': 'test body',
                    'answer': "test answer",
                    'category': 1,
        }
        request = self.factory.post(
            '/news/api/faq/', data, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)

        response.render()
        expected_respone = {'id': 3, 'title': 'test title', 'body': 'test body',
                            'answer': 'test answer', 'target_departament': 'non', 'target_location': 'non', 'category': 1}

        self.assertEquals(json.loads(response.content), expected_respone)
        self.assertEquals(DocQuestion.objects.count(), 3)
        self.assertEquals(response.status_code, 201)

    def test_view_object_creation_no_permission(self):
        user = self.test_user2
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)
        data = {
            'title': "test title",
            'body': 'test body',
                    'answer': "test answer",
                    'category': 1,
        }
        request = self.factory.post(
            '/news/api/faq/', data, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)

        response.render()

        expected_respone = {
            'detail': 'You do not have permission to perform this action.'}
        self.assertEquals(json.loads(response.content), expected_respone)
        self.assertEquals(DocQuestion.objects.count(), 2)
        self.assertEquals(response.status_code, 403)

    def test_view_object_update(self):
        user = self.test_user1
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)
        data = {
            'title': "test title",
            'body': 'test body',
                    'answer': "test answer update",
                    'category': 1,
        }

        request = self.factory.patch(
            '/news/api/faq/?pk=2', data, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)

        response.render()

        expected_respone = {'id': 2, 'title': 'test title', 'body': 'test body',
                            'answer': 'test answer update', 'target_departament': 'sal', 'target_location': 'PZN', 'category': 1}
        #
        self.assertEquals(json.loads(response.content), expected_respone)

        self.assertEquals(response.status_code, 200)

    def test_view_object_update_no_permission(self):
        user = self.test_user2
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)
        data = {
            'title': "test title",
            'body': 'test body',
                    'answer': "test answer update",
                    'category': 1,
        }

        request = self.factory.patch(
            '/news/api/faq/?pk=2', data, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)

        response.render()

        self.assertEquals(response.status_code, 403)

    def test_view_object_delete(self):
        user = self.test_user1
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)

        request = self.factory.delete(
            '/news/api/faq/?pk=2', HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)

        response.render()

        self.assertEquals(DocQuestion.objects.count(), 1)
        self.assertEquals(response.status_code, 204)

    def test_view_object_delete_no_permission(self):
        user = self.test_user2
        view = DocQuestionListAPIView.as_view()
        token = get_token(user)

        request = self.factory.delete(
            '/news/api/faq/?pk=2', HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)

        response.render()

        self.assertEquals(DocQuestion.objects.count(), 2)
        self.assertEquals(response.status_code, 403)


class TestUserQuestionCreateAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        newgroup = Group.objects.create(name='Managers')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)

        cls.test_category = KnowledgeCategory.objects.create(
            title='Test Category')

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
        cls.factory = APIRequestFactory()

    def test_view_object_creation(self):
        user = self.test_user1
        view = UserQuestionCreateAPIView.as_view()
        token = get_token(user)
        data = {
            'title': "test title",
            'body': 'test body',
                    'category': 1,
        }
        request = self.factory.post(
            '/news/api/userquestion/', data, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)

        response.render()

        expected_respone = {'title': 'test title', 'body': 'test body'}

        self.assertEquals(json.loads(response.content), expected_respone)
        self.assertEquals(DocQuestion.objects.count(), 1)
        self.assertEquals(response.status_code, 201)


class TestDocFileCreateAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        newgroup = Group.objects.create(name='Managers')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)
        cls.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK')
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
        cls.test_category = KnowledgeCategory.objects.create(
            title='Test Category')

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
        cls.factory = APIRequestFactory()

    def test_view_object_creation_no_permission(self):
        user = self.test_user2

        view = DocFileCreateAPIView.as_view()
        token = get_token(user)
        file = SimpleUploadedFile(
            "test_file.pdf",
            b"these are the file contents!"
        )

        files = {
            'file': SimpleUploadedFile(
                "test_file.pdf",
                b"these are the file contents!"),
            'title': 'test title',
            'category': 1
        }
        request = self.factory.post(
            '/news/api/uploaddocfile/', data=files, HTTP_AUTHORIZATION='JWT ' + token, format='multipart')
        response = view(request)
        response.render()
        self.assertEquals(DocFile.objects.count(), 0)
        self.assertEquals(response.status_code, 403)

    def test_view_object_creation(self):
        user = self.test_user1

        view = DocFileCreateAPIView.as_view()
        token = get_token(user)
        file = SimpleUploadedFile(
            "test_file.pdf",
            b"these are the file contents!"
        )
        # with open (file.path, 'rb') as f:
        files = {
            'file': SimpleUploadedFile(
                "test_file.pdf",
                b"these are the file contents!"),
            'title': 'test title',
            'category': 1
        }
        request = self.factory.post(
            '/news/api/uploaddocfile/', data=files, HTTP_AUTHORIZATION='JWT ' + token, format='multipart')
        response = view(request)
        response.render()
        self.assertEquals(DocFile.objects.count(), 1)
        self.assertEquals(response.status_code, 201)


class TestNewsFileCreateAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        newgroup = Group.objects.create(name='Managers')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)
        cls.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK')
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
        cls.test_user1.groups.add(newgroup)

        cls.test_category = KnowledgeCategory.objects.create(
            title='Test Category')

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
        cls.factory = APIRequestFactory()

    def test_view_object_creation(self):
        user = self.test_user1

        view = NewsFileCreateAPIView.as_view()
        token = get_token(user)
        file = SimpleUploadedFile(
            "test_file.pdf",
            b"these are the file contents!"
        )
        # with open (file.path, 'rb') as f:
        files = {
            'file': SimpleUploadedFile(
                "test_file.pdf",
                b"these are the file contents!"),
        }
        request = self.factory.post(
            '/news/api/uploadnewsfile/', data=files, HTTP_AUTHORIZATION='JWT ' + token, format='multipart')
        response = view(request)
        response.render()
        self.assertEquals(NewsFile.objects.count(), 1)
        self.assertEquals(response.status_code, 201)

    def test_view_object_creation_no_permission(self):
        user = self.test_user2

        view = NewsFileCreateAPIView.as_view()
        token = get_token(user)
        file = SimpleUploadedFile(
            "test_file.pdf",
            b"these are the file contents!"
        )

        files = {
            'file': SimpleUploadedFile(
                "test_file.pdf",
                b"these are the file contents!"),
        }
        request = self.factory.post(
            '/news/api/uploadnewsfile/', data=files, HTTP_AUTHORIZATION='JWT ' + token, format='multipart')
        response = view(request)
        response.render()
        self.assertEquals(NewsFile.objects.count(), 0)
        self.assertEquals(response.status_code, 403)


class TestDocumentFViewSet(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        cls.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK')
        newgroup = Group.objects.create(name='Managers')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)
        # cls.test_user2.groups.add(newgroup)

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

        cls.factory = APIRequestFactory()

    def test_GET_if_no_permission(self):
        user = self.test_user2
        token = get_token(user)
        view = DocumentFViewSet.as_view({'get': 'list'})
        uri = reverse('news-api:documents-list')
        request = self.factory.get(
            uri, HTTP_AUTHORIZATION='JWT ' + token)

        response = view(request)
        self.assertEquals(response.status_code, 403)

    def test_GET_if_has_permission(self):
        view = DocumentFViewSet.as_view({'get': 'list'})
        uri = reverse('news-api:documents-list')
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            uri, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)
        self.assertEquals(response.status_code, 200)


class TestNewsViewSet(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        cls.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK')
        cls.test_user3 = User.objects.create_user(
            username='testuser3', password='1X<ISRUkw+tuK')
        newgroup = Group.objects.create(name='Managers')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)
        permission = Permission.objects.get(name="Can view news")
        permission_publish = Permission.objects.get(name="Can change news")
        cls.test_user1.groups.add(newgroup)
        cls.test_user3.groups.add(newgroup)
        cls.test_user2.user_permissions.add(permission)
        cls.test_user2.user_permissions.add(permission_publish)
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

        test_news = News.objects.create(
            title="test title",
            body='test body',
            author=cls.test_user1,
            target_location="PZN",
            target_departament="sal",

        )
        test_news2 = News.objects.create(
            title="test title",
            body='test body',
            author=cls.test_user1,


        )
        test_news3 = News.objects.create(
            title="test title",
            body='test body',
            author=cls.test_user1,

        )
        test_news.publish()
        test_news2.publish()

        cls.factory = APIRequestFactory()

    def test_view_queryset_response(self):
        view = NewsViewSet.as_view({'get': 'list'})
        uri = reverse('news-api:news-list')
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            uri, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)
        response.render()

        self.assertEquals(response.status_code, 200)

        self.assertEquals(json.loads(response.content)[0]['id'], 2)
        self.assertEquals(json.loads(response.content)[1]['id'], 3)
        user = self.test_user2
        token = get_token(user)
        request = self.factory.get(
            uri, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)
        response.render()

        self.assertEquals(json.loads(response.content)[0]['id'], 2)
        self.assertEquals(json.loads(response.content)[1]['id'], 1)

    def test_view_publish_action(self):
        view = NewsViewSet.as_view({'get': 'list'})
        uri = reverse('news-api:news-list')
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            uri, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request)
        response.render()

        self.assertEquals(len(json.loads(response.content)), 2)

        view = NewsViewSet.as_view({'get': 'publish'},
                                   detail=True)
        uri_publish = reverse('news-api:news-publish', kwargs={'pk': '3'})

        request_publish = self.factory.get(
            uri_publish, HTTP_AUTHORIZATION='JWT ' + token)
        response = view(request_publish, pk=3)
        response.render()

        user = self.test_user2
        token = get_token(user)
        request = self.factory.get(
            uri, HTTP_AUTHORIZATION='JWT ' + token)
        view = NewsViewSet.as_view({'get': 'list'})
        response = view(request)
        response.render()
        self.assertEquals(len(json.loads(response.content)), 3)
