from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import change_password, UserProfileDetailView, EmployeeListView, user_login, user_logout, edit_profile, delete_profile_pic


class TestUrls(SimpleTestCase):

    def test_employees_url_resolves(self):
        url = reverse('accounts:employees')
        self.assertEquals(resolve(url).func.view_class,EmployeeListView)

    def test_user_login_url_resolves(self):
        url = reverse('accounts:user_login')
        self.assertEquals(resolve(url).func,user_login)

    def test_user_logout_url_resolves(self):
        url = reverse('accounts:user_logout')
        self.assertEquals(resolve(url).func,user_logout)


    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertEquals(resolve(url).func.view_class,UserProfileDetailView)

    def test_edit_profile_login_url_resolves(self):
        url = reverse('accounts:edit_profile')
        self.assertEquals(resolve(url).func,edit_profile)

    def test_change_password_url_resolves(self):
        url = reverse('accounts:change_password')
        self.assertEquals(resolve(url).func,change_password)

    def test_delete_profile_pic_url_resolves(self):
        url = reverse('accounts:delete_profile_pic')
        self.assertEquals(resolve(url).func,delete_profile_pic)
