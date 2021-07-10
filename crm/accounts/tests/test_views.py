from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden
class TestAccountsViews(TestCase):

    def setUp(self):

        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user3 = User.objects.create_user(username='testuser3', password='2HJ1vRVkw+3iD')
        test_user4 = User.objects.create_user(username='testuser4', password='2Hkw+RV0Z&3iD')

        test_user1.save()
        test_user2.save()
        test_user3.save()
        test_user4.save()


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
            telephone='22',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
             )

        test_user3_userprofile = UserProfile.objects.create(
            user=test_user3,
            name='Test User3',
            telephone='33',
            email='testuser3@email.com',
            employee_id='4',
            departament='mar',
            location='KRK',
             )

        test_user4_userprofile = UserProfile.objects.create(
            user=test_user4,
            name='Test User4',
            telephone='44',
            email='testuser4@email.com',
            employee_id='5',
            departament='HR',
            location='KRK'
            )


        test_user1_userprofile.save()
        test_user2_userprofile.save()
        test_user3_userprofile.save()
        test_user4_userprofile.save()


        self.list_url = 'accounts:employees'
        self.user_login = 'accounts:user_login'
        self.user_detail = 'accounts:profile'
        self.edit_profile = 'accounts:edit_profile'
    # def test_user_login(self):
    #     response = self.client.post(self.user_login, {
    #     'username' : 'testuser',
    #     'password' : '1X<ISRUkw+tuK'
    #     })
    #     print(response)

    def test_EmployeeListView_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(self.list_url))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/employees/')



    def test_EmployeeListView_GET_logged_in(self):

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse(self.list_url))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'accounts/userprofile_list.html')
        self.assertEquals(response.context['object_list'].count(), 4)
        # response = self.client.get(reverse('accounts:employees',args=['q':str(3)]))

    def test_UserProfileDetailView_if_not_logged_in(self):
        response = self.client.get(reverse(self.user_detail))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile')

    def test_UserProfileDetailView_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse(self.user_detail))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'accounts/userprofile_detail.html')

    def test_edit_profile_not_logged_in(self):
        response = self.client.get(reverse(self.edit_profile))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/edit')

    def test_edit_profile_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse(self.edit_profile))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'accounts/editprofile.html')

    # def test_edit_profile_POST_add_new_profile_pic(self):
    #     login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    #     response = self.client.POST(self.edit_profile,{
    #         profile_pic =
    #     })
