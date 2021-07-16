from django.test import TestCase
from accounts.models import UserProfile
from django.contrib.auth.models import User
from calendary.models import Day,Devent
from datetime import date, timedelta

class CalendarModelsTest(TestCase):


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

        self.test_date = date(2019, 12, 1)
        self.test_day = Day.objects.create(date = self.test_date)

        self.test_devent = Devent.objects.create(
            day = self.test_day,
            title = 'test devent title',
            description = 'test devent description',
            author = test_user1,
        )

    def test_day_date_label(self):
        field_label = self.test_day._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_day_object_name(self):
        expected_object_name = self.test_day.date.strftime('%m/%d/%Y')
        self.assertEqual(str(self.test_day), expected_object_name)

    def test_devent_day_label(self):
        field_label = self.test_devent._meta.get_field('day').verbose_name
        self.assertEqual(field_label, 'day')

    def test_devent_title_label(self):
        field_label = self.test_devent._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_devent_description_label(self):
        field_label = self.test_devent._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_devent_start_label(self):
        field_label = self.test_devent._meta.get_field('start').verbose_name
        self.assertEqual(field_label, 'Start time')

    def test_devent_end_label(self):
        field_label = self.test_devent._meta.get_field('end').verbose_name
        self.assertEqual(field_label, 'Ending time')


    def test_devent_author_label(self):
        field_label = self.test_devent._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_devent_object_name(self):
        expected_object_name = '{0} ({1})'.format(self.test_devent.title, self.test_day)
        self.assertEqual(str(self.test_devent), expected_object_name)

    def test_devent_get_absolute_url(self):
        self.assertEqual(self.test_devent.get_absolute_url(), '/calendar/event/1')

    def test_devent_title_max_length(self):
        max_length= self.test_devent._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_devent_title_max_length(self):
        max_length= self.test_devent._meta.get_field('description').max_length
        self.assertEqual(max_length, 5000)
