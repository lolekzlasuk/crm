from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
from datetime import date, timedelta
from news.models import KnowledgeCategory, DocumentF, DocFile
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

class TestKnowledgeCategoryListView(TestCase):


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

        test_user1_userprofile.save()

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




class TestKnowledgeCategoryDetailView(TestCase):



    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')

        test_user1.save()
        test_user2.save()
        # test_group = Group.objects.create(name="test_group")
        #
        # test_user2.groups.add(test_group)
        # test_user2.save()

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='111111111',
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
            departament='HR',
            location='WAW'
            )

        test_user1_userprofile.save()

        test_user2_userprofile.save()

        cls.test_category = KnowledgeCategory.objects.create(title="Test Category")

        
        cls.test_document_1 = KnowledgeCategory.objects.create()

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
































    # def test_view_redirect_if_not_logged_in(self):
    #     response = self.client.get(reverse('calendary:post_devent', kwargs={'pk': self.test_day.pk}))
    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, '/accounts/login/?next=/calendar/153/addevent/')
    #
    #
    # def test_view_redirect_if_logged_in_no_permission(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.get(reverse('calendary:post_devent', kwargs={'pk': self.test_devent.pk}))
    #     self.assertEquals(response.status_code, 403)
    #
    #
    # def test_view_redirect_if_logged_in_has_permission(self):
    #     login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
    #
    #     response = self.client.get(reverse('calendary:post_devent', kwargs={'pk': self.test_devent.pk}))
    #
    #
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'calendary/deventform.html')
