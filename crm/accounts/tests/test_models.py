from django.test import TestCase, override_settings
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
import shutil
from django.conf import settings
MEDIA_ROOT = tempfile.mkdtemp()

# user
# profile_pic
# name
# telephone
# email
# date_of_employement
# employee_id
# position
# departament
# location

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class UserProfileModelTest(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')

        test_user1.save()
        cls.test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='111111111',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
            )

        # test_image_path = settings.MEDIA_DIR + '/test_image/dino.jpg'
        # cls.test_image = open(test_image_path, 'rb')
        # cls.simple_file_image = SimpleUploadedFile(name = "testimage.jpg",  content=open(test_image_path, 'rb').read(), content_type='image/jpeg')

        # user
        # profile_pic
        # name
        # telephone
        # email
        # date_of_employement
        # employee_id
        # position
        # departament
        # location
    def test_userprofile_user_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_userprofile_profile_pic_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('profile_pic').verbose_name
        self.assertEqual(field_label, 'profile pic')

    def test_userprofile_name_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_userprofile_telephone_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('telephone').verbose_name
        self.assertEqual(field_label, 'telephone')

    def test_userprofile_email_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_userprofile_date_of_employement_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('date_of_employement').verbose_name
        self.assertEqual(field_label, 'date of employement')

    def test_userprofile_employee_id_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('employee_id').verbose_name
        self.assertEqual(field_label, 'employee id')

    def test_userprofile_position_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('position').verbose_name
        self.assertEqual(field_label, 'position')

    def test_userprofile_departament_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('departament').verbose_name
        self.assertEqual(field_label, 'departament')

    def test_userprofile_location_label(self):
        field_label = self.test_user1_userprofile._meta.get_field('location').verbose_name
        self.assertEqual(field_label, 'location')

    def test_userprofile_name_max_length(self):
        max_length= self.test_user1_userprofile._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_userprofile_email_max_length(self):
        max_length= self.test_user1_userprofile._meta.get_field('email').max_length
        self.assertEqual(max_length, 200)

    def test_userprofile_employee_id_max_length(self):
        max_length= self.test_user1_userprofile._meta.get_field('employee_id').max_length
        self.assertEqual(max_length, 20)

    def test_userprofile_position_max_length(self):
        max_length= self.test_user1_userprofile._meta.get_field('position').max_length
        self.assertEqual(max_length, 40)

    def test_userprofile_departament_max_length(self):
        max_length= self.test_user1_userprofile._meta.get_field('departament').max_length
        self.assertEqual(max_length, 3)

    def test_userprofile_location_max_length(self):
        max_length= self.test_user1_userprofile._meta.get_field('location').max_length
        self.assertEqual(max_length, 3)

    def test_user1_userprofile_object_name(self):
        expected_object_name = 'Test User1'

        self.assertEqual(str(self.test_user1_userprofile), expected_object_name)

    # def test_user1_userprofile_resize_file(self):
    #     print(self.test_user1_userprofile.profile_pic.path)
    #     self.test_user1_userprofile.change_profile_pic(self.test_image)
    #
    #     # expected_miniature_path = '/media/upload/thumbs/testimage-thumb.jpg'
    #     print(self.test_user1_userprofile.profile_pic.path)
    #     # self.assertEqual(self.test_user1_userprofile_2.miniature, expected_miniature_path)
    #
    # def test_user1_userprofile_miniature_size(self):
    #     expected_miniature_size = 128,128
    #     miniature_path = settings.MEDIA_DIR + '/upload/thumbs/testimage-thumb.jpg'
    #     image = Image.open(miniature_path)
    #     self.assertEqual(image.size, expected_miniature_size)
