from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Permission, Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from accounts.models import UserProfile
from news.models import KnowledgeCategory, DocumentF, DocQuestion, DocFile, \
    NewsFile, DocumentF, News, NotificationReadFlag
from datetime import date, timedelta
import json
import tempfile
import shutil

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestKnowledgeCategoryListView(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )

        test_user1_userprofile.save()
        test_user2_userprofile.save()
        cls.test_category = KnowledgeCategory.objects.create(title='Test Category')
        cls.test_category_2 = KnowledgeCategory.objects.create(title='Test Category 2')
        i = 0
        file_test_category = cls.test_category

        while i < 11:
            if i%2 == 0:
                test_location = 'WAW'
            elif i%3 == 0:
                test_location = 'non'
            else:
                test_location = 'PZN'

            if i%4 == 0:
                test_departament = 'HR'
            elif i%3 == 0:
                test_departament = 'non'
            else:
                test_departament = 'sal'


            instance = DocFile.objects.create(
                file = SimpleUploadedFile(
                    'best_dasdasasdds.txt',
                    b'these are the file contents!'
                ),
                title = 'test title',
                date_created = timezone.now(),
                target_departament = test_departament,
                target_location  = test_location,
                category = file_test_category)
            instance.save()

            instance = DocumentF.objects.create(

                title = 'test title',
                body = 'test body',
                author = test_user1,
                date_created = timezone.now(),
                target_departament = test_departament,
                target_location  = test_location,
                category = file_test_category)
            instance.save()
            i +=1



    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:knowledge'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/knowledge/')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:knowledge'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/knowledgecategory_list.html')

    def test_view_if_files_filtered(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:knowledge'))
        self.assertEquals(response.context['files'].count(),6)

    def test_view_if_files_filtered_2(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:knowledge'))
        self.assertEquals(response.context['files'].count(),5)

    def test_view_if_documents_filtered(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:knowledge'))
        self.assertEquals(response.context['docs'].count(),6)

    def test_view_if_documents_filtered_2(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:knowledge'))
        self.assertEquals(response.context['docs'].count(),5)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestKnowledgeCategoryDetailView(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )

        test_user1_userprofile.save()
        test_user2_userprofile.save()
        cls.test_category = KnowledgeCategory.objects.create(title='Test Category')
        cls.test_category_2 = KnowledgeCategory.objects.create(title='Test Category 2')
        cls.test_category.save()
        cls.test_category_2.save()
        i = 0
        file_test_category = cls.test_category

        while i < 11:
            if i%2 == 0:
                test_location = 'WAW'
                file_test_category = cls.test_category_2
            elif i%3 == 0:
                test_location = 'non'
                file_test_category = cls.test_category_2
            else:
                test_location = 'PZN'

            if i%4 == 0:
                test_departament = 'HR'
            elif i%3 == 0:
                test_departament = 'non'
            else:
                test_departament = 'sal'
            # print(test_location + '  ' + test_departament + '  ' + file_test_category.title)

            instance = DocFile.objects.create(
                file = SimpleUploadedFile(
                    'best_file_eva.txt',
                    b'these are the file contents!'
                ),
                title = 'test title',
                date_created = timezone.now(),
                target_departament = test_departament,
                target_location  = test_location,
                category = file_test_category)
            instance.save()

            instance = DocumentF.objects.create(

                title = 'test title',
                body = 'test body',
                author = test_user1,
                date_created = timezone.now(),
                target_departament = test_departament,
                target_location  = test_location,
                category = file_test_category)
            instance.save()
            file_test_category = cls.test_category
            i +=1


    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:knowledgedetail',kwargs={'pk':self.test_category.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/knowledge/1')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:knowledgedetail',kwargs={'pk':self.test_category.pk}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/knowledgecategory_detail.html')

    def test_view_if_files_filtered_by_category(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:knowledgedetail',kwargs={'pk':self.test_category_2.pk}))
        self.assertEquals(response.context['files'].count(),6)

    def test_view_if_files_filtered_by_category_2(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:knowledgedetail',kwargs={'pk':self.test_category_2.pk}))
        self.assertEquals(response.context['files'].count(),2)

    def test_view_if_documents_filtered_by_category(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:knowledgedetail',kwargs={'pk':self.test_category_2.pk}))
        self.assertEquals(response.context['docs'].count(),6)

    def test_view_if_documents_filtered_by_category_2(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:knowledgedetail',kwargs={'pk':self.test_category_2.pk}))
        self.assertEquals(response.context['docs'].count(),2)

    def test_view_if_categories_queryset(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:knowledgedetail',kwargs={'pk':self.test_category_2.pk}))
        self.assertEquals(response.context['categories'].count(),2)





class TestQuestionsListView(TestCase):


    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )

        test_user1_userprofile.save()
        test_user2_userprofile.save()
        cls.test_category = KnowledgeCategory.objects.create(title='Test Category')
        cls.test_category_2 = KnowledgeCategory.objects.create(title='Test Category 2')
        cls.test_category.save()
        cls.test_category_2.save()
        i = 0
        file_test_category = cls.test_category

        while i < 11:
            if i%2 == 0:
                test_location = 'WAW'
                file_test_category = cls.test_category_2
            elif i%3 == 0:
                test_location = 'non'
                file_test_category = cls.test_category_2
            else:
                test_location = 'PZN'

            if i%4 == 0:
                test_departament = 'HR'
            elif i%3 == 0:
                test_departament = 'non'
            else:
                test_departament = 'sal'

            # print('%s %s %s' %(test_location,test_departament,file_test_category))

            instance = DocQuestion.objects.create(

                title = 'test title',
                body = 'test body',
                answer = 'test answer',
                date_created = timezone.now(),
                target_departament = test_departament,
                target_location  = test_location,
                category = file_test_category)
            instance.save()
            file_test_category = cls.test_category
            i +=1





    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:faq'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/faq/')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:faq'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/docquestion_list.html')

    # def test_view_queryset_length(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('news:faq'))
    #     self.assertEquals(response.context['object_list'].count(),6)

    def test_view_if_files_filtered_by_category_2(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get('%s?category=%s' % (reverse('news:faq'),2))
        self.assertEquals(response.context['object_list'].count(),3)

    def test_view_if_files_filtered_by_category_1(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get('%s?category=%s' % (reverse('news:faq'),1))
        self.assertEquals(response.context['object_list'].count(),3)

    def test_view_if_filtered_by_location_depratament_1(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:faq'))
        self.assertEquals(response.context['object_list'].count(),8)

    def test_view_if_filtered_bylocation_depratament_2(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:faq'))
        self.assertEquals(response.context['object_list'].count(),6)

    def test_view_categories_queryset(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:faq'))
        self.assertEquals(response.context['categories'].count(),2)







#
#
# class TestUnansweredQuestionsListView(TestCase):
#
#
#     @classmethod
#     def setUpTestData(cls):
#         test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
#         test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
#         test_user2.save()
#         test_user1.save()
#
#         test_user1_userprofile = UserProfile.objects.create(
#             user=test_user1,
#             name='Test User1',
#             telephone='11',
#             email='testuser1@email.com',
#             employee_id='2',
#             departament='HR',
#             location='WAW'
#             )
#
#         test_user2_userprofile = UserProfile.objects.create(
#             user=test_user2,
#             name='Test User2',
#             telephone='222222222',
#             email='testuser2@email.com',
#             employee_id='3',
#             departament='sal',
#             location='PZN'
#             )
#
#         test_user1_userprofile.save()
#         test_user2_userprofile.save()
#         UserQuestion.objects.create(
#             title='test title',
#             body='test body',
#             author= test_user1
#         )
#         permission = Permission.objects.get(name='Can view user question')
#         test_user2.user_permissions.add(permission)
#         test_user2.save()
#
#     def test_view_redirect_if_not_logged_in(self):
#         response = self.client.get(reverse('news:pending_faq'))
#         self.assertEquals(response.status_code, 302)
#         self.assertRedirects(response, '/accounts/login/?next=/faq/pending/')
#
#     def test_view_if_logged_in_no_permission(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.get(reverse('news:pending_faq'))
#         self.assertEquals(response.status_code, 403)
#
#     def test_view_if_logged_in_with_permission(self):
#         login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
#         response = self.client.get(reverse('news:pending_faq'))
#         self.assertEquals(response.status_code, 200)
#         self.assertEqual(str(response.context['user']), 'testuser2')
#         self.assertTemplateUsed(response, 'news/pending_questions.html')
#
#     def test_view_queryset_length(self):
#         login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
#         response = self.client.get(reverse('news:pending_faq'))
#         self.assertEqual(response.context['object_list'].count(), 1)
#



class TestUnpublishedNewsListView(TestCase):


    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )

        test_user1_userprofile.save()
        test_user2_userprofile.save()
        i = 0
        while i < 4:

            instance = News.objects.create(
                title='test title',
                body='test body',
                author= test_user1
            )
            instance.save()
            i +=1
        instance.publish()

        permission = Permission.objects.get(name='Can add news')
        test_user2.user_permissions.add(permission)
        test_user2.save()



    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:unpublished'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/news/unpublished/')

    def test_view_if_logged_in_no_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:unpublished'))
        self.assertEquals(response.status_code, 403)

    def test_view_if_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:unpublished'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/news_list.html')

    def test_view_queryset_length(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:unpublished'))
        self.assertEqual(str(response.context['object_list'].count()), '3')


class TestNewsDetailView(TestCase):


    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user3 = User.objects.create_user(username='testuser3', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()
        test_user3.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='sal',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )
        test_user3_userprofile = UserProfile.objects.create(
            user=test_user3,
            name='Test User3',
            telephone='333333333',
            email='testuser3@email.com',
            employee_id='4',
            departament='mar',
            location='PZN'
            )
        test_user1_userprofile.save()
        test_user2_userprofile.save()
        test_user3_userprofile.save()
        cls.test_news = News.objects.create(
            title='test title',
            body='test body',
            author= test_user1,
            target_location = 'PZN',
            target_departament = 'sal'
        )

        cls.test_news.publish()


    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:newsdetail',kwargs={'pk':self.test_news.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/news/1/')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:newsdetail',kwargs={'pk':self.test_news.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/news_detail.html')

    def test_view_wrong_departament(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:newsdetail',kwargs={'pk':self.test_news.pk}))
        self.assertEquals(response.status_code, 403)


    def test_view_wrong_location(self):
        login = self.client.login(username='testuser3', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:newsdetail',kwargs={'pk':self.test_news.pk}))
        self.assertEquals(response.status_code, 403)

class TestDocDetailView(TestCase):


    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user3 = User.objects.create_user(username='testuser3', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()
        test_user3.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='sal',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )
        test_user3_userprofile = UserProfile.objects.create(
            user=test_user3,
            name='Test User3',
            telephone='333333333',
            email='testuser3@email.com',
            employee_id='4',
            departament='mar',
            location='PZN'
            )
        test_user1_userprofile.save()
        test_user2_userprofile.save()
        test_user3_userprofile.save()

        cls.test_category = KnowledgeCategory.objects.create(title='Test Category')
        cls.test_category_2 = KnowledgeCategory.objects.create(title='Test Category 2')
        cls.test_category.save()
        cls.test_category_2.save()
        cls.test_document = DocumentF.objects.create(
            title='test title',
            body='test body',
            author= test_user1,
            target_location = 'PZN',
            target_departament = 'sal'
        )




    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:docdetail',kwargs={'pk':self.test_document.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/docs/1/')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:docdetail',kwargs={'pk':self.test_document.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/documentf_detail.html')

    def test_view_wrong_departament(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:docdetail',kwargs={'pk':self.test_document.pk}))
        self.assertEquals(response.status_code, 403)


    def test_view_wrong_location(self):
        login = self.client.login(username='testuser3', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:docdetail',kwargs={'pk':self.test_document.pk}))
        self.assertEquals(response.status_code, 403)




class TestNewsListView(TestCase):


    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )

        test_user1_userprofile.save()
        test_user2_userprofile.save()
        i = 0
        while i < 4:

            instance = News.objects.create(
                title='test title',
                body='test body',
                author= test_user1
            )
            instance.save()
            i +=1
            instance.publish()
        instance.published_date = None
        instance.save()

        i = 0
        while i < 11:
            if i%2 == 0:
                test_location = 'WAW'

            elif i%3 == 0:
                test_location = 'non'
            else:
                test_location = 'PZN'

            if i%5 == 0:
                test_departament = 'HR'
            else:
                test_departament = 'mar'

            instance = News.objects.create(
                title='test title',
                body='test body',
                author= test_user1,
                target_location=test_location,
                target_departament=test_departament,
            )
            i +=1
            # print('%s, %s' %(instance.target_location,instance.target_departament))
            instance.publish()



    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:news_list'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:news_list'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/news_list.html')

    def test_view_queryset_filtering(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:news_list'))
        self.assertEqual(str(response.context['object_list'].count()), '7')

    def test_view_queryset_filtering(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:news_list'))
        self.assertEqual(str(response.context['object_list'].count()), '9')

class TestPostNewsView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        permission = Permission.objects.get(name='Can add news')
        test_user2.user_permissions.add(permission)
        test_user2.save()


    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:post_news'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/upload/news')

    def test_view_if_logged_in_no_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:post_news'))
        self.assertEquals(response.status_code, 403)

    def test_view_if_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:post_news'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/upload.html')


class TestPublishNewsView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )
        permission = Permission.objects.get(name='Can add news')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        cls.test_news = News.objects.create(
            title='test title',
            body='test body',
            author= test_user1,
        )

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:publish_news',kwargs={'pk':self.test_news.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/news/1/publish/')

    def test_view_if_logged_in_no_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:publish_news',kwargs={'pk':self.test_news.pk}))
        self.assertEquals(response.status_code, 403)

    def test_view_if_redirect_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:publish_news',kwargs={'pk':self.test_news.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_view_if_publish(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:publish_news',kwargs={'pk':self.test_news.pk}))
        self.test_news.refresh_from_db()
        self.assertIsNotNone(self.test_news.published_date)



class TestAnswerFaqView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )
        permission = Permission.objects.get(name='Can view user question')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        cls.test_userquestion = UserQuestion.objects.create(
            title='test title',
            body='test body',
            author= test_user1,
        )

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:answerfaq',kwargs={'pk':self.test_userquestion.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/upload/1/updatequestion')

    def test_view_if_logged_in_no_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:answerfaq',kwargs={'pk':self.test_userquestion.pk}))
        self.assertEquals(response.status_code, 403)

    def test_view_if_redirect_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:answerfaq',kwargs={'pk':self.test_userquestion.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/upload.html')

class TestFlagToggleView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )


        cls.test_news = News.objects.create(
            title='test title',
            body='test body',
            author= test_user1,
        )
        cls.test_news.publish()
        cls.test_notification = Notification.objects.get(news=cls.test_news)
        cls.test_notificationreadflag = NotificationReadFlag.objects.get(
                            user=test_user1, notification=cls.test_notification)
        # cls.test_newsreadflag = NewsReadFlag.objects.get(user=test_user1, news=cls.test_news)
        cls.json_data = json.dumps({'pk': cls.test_news.pk})

    def test_view_redirect_if_not_logged_in(self):


        response = self.client.post(reverse('news:flagtoggle'), self.json_data,
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/flagtoggle/')

    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('news:flagtoggle'), self.json_data,
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_view_if_notificationreadflag_true(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('news:flagtoggle'), self.json_data,
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.test_notificationreadflag.refresh_from_db()
        self.assertTrue(self.test_notificationreadflag.read)

    # def test_view_if_newsreadflag_true(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.post(reverse('news:flagtoggle'), self.json_data,
    #             content_type='application/json',
    #             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #
    #     self.test_newsreadflag.refresh_from_db()
    #     self.assertTrue(self.test_newsreadflag.read)

#
# class TestNewsReadFlagToggleView(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
#         test_user1.save()
#
#         test_user1_userprofile = UserProfile.objects.create(
#             user=test_user1,
#             name='Test User1',
#             telephone='11',
#             email='testuser1@email.com',
#             employee_id='2',
#             departament='HR',
#             location='WAW'
#             )
#
#
#         cls.test_news = News.objects.create(
#             title='test title',
#             body='test body',
#             author= test_user1,
#         )
#         cls.test_news.publish()
#         cls.test_newsreadflag = NewsReadFlag.objects.get(user=test_user1, news=cls.test_news)
#         cls.json_data = json.dumps({'pk': cls.test_news.pk})
#
#     def test_view_redirect_if_not_logged_in(self):
#
#
#         response = self.client.post(reverse('news:newsreadflag'), self.json_data,
#                 content_type='application/json',
#                 HTTP_X_REQUESTED_WITH='XMLHttpRequest')
#         self.assertEquals(response.status_code, 302)
#         self.assertRedirects(response, '/accounts/login/?next=/newstoggle/')
#
#     def test_view_if_logged_in(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.post(reverse('news:newsreadflag'), self.json_data,
#                 content_type='application/json',
#                 HTTP_X_REQUESTED_WITH='XMLHttpRequest')
#         self.assertEquals(response.status_code, 200)
#
#     def test_view_if_newsreadflag_true(self):
#         login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
#         response = self.client.post(reverse('news:newsreadflag'), self.json_data,
#                 content_type='application/json',
#                 HTTP_X_REQUESTED_WITH='XMLHttpRequest')
#
#         self.test_newsreadflag.refresh_from_db()
#         self.assertTrue(self.test_newsreadflag.read)
#
#

class TestMarkallView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )


        cls.test_news = News.objects.create(
            title='test title',
            body='test body',
            author= test_user1,
        )
        cls.test_news_2 = News.objects.create(
            title='test title 2',
            body='test body',
            author= test_user1,
        )
        cls.test_news.publish()
        cls.test_notification = Notification.objects.get(news=cls.test_news)
        cls.test_notificationreadflag = NotificationReadFlag.objects.get(
                            user=test_user1, notification=cls.test_notification)
        # cls.test_newsreadflag = NewsReadFlag.objects.get(user=test_user1, news=cls.test_news)


        cls.test_news_2.publish()
        cls.test_notification_2 = Notification.objects.get(news=cls.test_news_2)
        cls.test_notificationreadflag_2 = NotificationReadFlag.objects.get(
                            user=test_user1, notification=cls.test_notification_2)
        # cls.test_newsreadflag_2 = NewsReadFlag.objects.get(user=test_user1, news=cls.test_news_2)
        cls.json_data = json.dumps({})

    def test_view_redirect_if_not_logged_in(self):

        response = self.client.post(reverse('news:markall'), self.json_data,
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/markall/')

    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('news:markall'), self.json_data,
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_view_if_notificationreadflag_true(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('news:markall'), self.json_data,
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.test_notificationreadflag.refresh_from_db()
        self.assertTrue(self.test_notificationreadflag.read)
        self.test_notificationreadflag_2.refresh_from_db()
        self.assertTrue(self.test_notificationreadflag_2.read)

    # def test_view_if_newsreadflag_true(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.post(reverse('news:markall'), self.json_data,
    #             content_type='application/json',
    #             HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # self.test_newsreadflag.refresh_from_db()
        # self.assertTrue(self.test_newsreadflag.read)
        # self.test_newsreadflag_2.refresh_from_db()
        # self.assertTrue(self.test_newsreadflag_2.read)



class TestPostDocumentView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        permission = Permission.objects.get(name='Can add document f')
        test_user2.user_permissions.add(permission)
        test_user2.save()


    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:createdoc'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/upload/doc')

    def test_view_if_logged_in_no_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:createdoc'))
        self.assertEquals(response.status_code, 403)

    def test_view_if_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:createdoc'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/upload.html')


class TestPostDocFileView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        permission = Permission.objects.get(name='Can add doc file')
        test_user2.user_permissions.add(permission)
        test_user2.save()


    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:createfile'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/upload/file')

    def test_view_if_logged_in_no_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:createfile'))
        self.assertEquals(response.status_code, 403)

    def test_view_if_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:createfile'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/upload.html')


class TestPostQuestionView(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()
        test_user1.save()

        permission = Permission.objects.get(name='Can add doc question')
        test_user2.user_permissions.add(permission)
        test_user2.save()


    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:createquestion'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/upload/question')

    def test_view_if_logged_in_no_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('news:createquestion'))
        self.assertEquals(response.status_code, 403)

    def test_view_if_logged_in_with_permission(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:createquestion'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/upload.html')

class TestPostUserQuestionView(TestCase):

    @classmethod
    def setUpTestData(cls):

        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')
        test_user2.save()


    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('news:createuserquestion'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/upload/userquestion')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('news:createuserquestion'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertTemplateUsed(response, 'news/upload.html')
