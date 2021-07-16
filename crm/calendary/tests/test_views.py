from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
from datetime import date, timedelta
from calendary.models import Day, Devent
from django.contrib.auth.models import Permission


class TestDayListView(TestCase):

    def setUp(self):
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

        start_date = date(2019, 12, 1)
        end_date = date(2021, 1, 30)
        delta = timedelta(days=1)
        while start_date <= end_date:
            Day.objects.create(date=start_date)
            start_date += delta

        self.list_url = '/calendar/2020/6/'

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.list_url)
        self.assertRedirects(response, '/accounts/login/?next=/calendar/2020/6/')

    def test_view_GET_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'calendary/day_list.html')

    def test_view_proper_queryset_length(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        for each in range(1,12):
            response = self.client.get(reverse('calendary:calendary',kwargs={ 'year':'2020', 'month':each}))
            self.assertEquals(response.context['object_list'].count() %7, 0)

class TestDayDetailView(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        start_date = date(2019, 12, 1)
        end_date = date(2021, 1, 30)
        delta = timedelta(days=1)
        while start_date <= end_date:
            Day.objects.create(date=start_date)
            start_date += delta

        test_date = date(2020, 5, 1)
        self.test_day = Day.objects.get(date = test_date)

        self.test_devent = Devent.objects.create(day=self.test_day,
            title='test devent',
            author=test_user1,
            description='trr',
            start = '00:00',
            end = '12:00')

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('calendary:devent', kwargs={'pk': self.test_day.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/calendar/event/153')

    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('calendary:devent', kwargs={'pk': self.test_devent.pk}))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendary/devent_detail.html')

class TestPOST_Devent_View(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')

        test_user1.save()
        test_user2.save()

        permission = Permission.objects.get(name='Can add devent')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        start_date = date(2019, 12, 1)
        end_date = date(2021, 1, 30)
        delta = timedelta(days=1)
        while start_date <= end_date:
            Day.objects.create(date=start_date)
            start_date += delta

        test_date = date(2020, 5, 1)
        self.test_day = Day.objects.get(date = test_date)
        self.test_devent = Devent.objects.create(day=self.test_day,
            title='test devent',
            author=test_user2,
            description='trr',
            start = '00:00',
            end = '12:00')

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('calendary:post_devent', kwargs={'pk': self.test_day.pk}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/calendar/153/addevent/')

    def test_view_redirect_if_logged_in_no_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('calendary:post_devent', kwargs={'pk': self.test_devent.pk}))
        self.assertEquals(response.status_code, 403)

    def test_view_redirect_if_logged_in_has_permission(self):
        login = self.client.login(username='testuser2', password='1ddsSRUkw+tuK')
        response = self.client.get(reverse('calendary:post_devent', kwargs={'pk': self.test_devent.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendary/deventform.html')
