from django.test import TestCase, override_settings
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from news.models import KnowledgeCategory, DocumentF, DocQuestion, DocFile, \
    NewsFile, DocumentF, News, NotificationReadFlag
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
import shutil
MEDIA_ROOT = tempfile.mkdtemp()


class NewsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

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
            author=test_user1,
        )
        cls.test_news.save()

    def test_news_body_label(self):
        field_label = self.test_news._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_news_title_label(self):
        field_label = self.test_news._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_news_date_created_label(self):
        field_label = self.test_news._meta.get_field(
            'date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_news_author_label(self):
        field_label = self.test_news._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_news_published_date_label(self):
        field_label = self.test_news._meta.get_field(
            'published_date').verbose_name
        self.assertEqual(field_label, 'published date')

    def test_news_files_label(self):
        field_label = self.test_news._meta.get_field('files').verbose_name
        self.assertEqual(field_label, 'files')

    def test_news_target_departament_label(self):
        field_label = self.test_news._meta.get_field(
            'target_departament').verbose_name
        self.assertEqual(field_label, 'target departament')

    def test_news_target_location_label(self):
        field_label = self.test_news._meta.get_field(
            'target_location').verbose_name
        self.assertEqual(field_label, 'target location')

    def test_news_slug_label(self):
        field_label = self.test_news._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_news_title_max_length(self):
        max_length = self.test_news._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_news_body_max_length(self):
        max_length = self.test_news._meta.get_field('body').max_length
        self.assertEqual(max_length, 5000)

    def test_news_target_location_max_length(self):
        max_length = self.test_news._meta.get_field(
            'target_location').max_length
        self.assertEqual(max_length, 3)

    def test_news_target_departament_max_length(self):
        max_length = self.test_news._meta.get_field(
            'target_departament').max_length
        self.assertEqual(max_length, 3)

    def test_news_slug_max_length(self):
        max_length = self.test_news._meta.get_field('slug').max_length
        self.assertEqual(max_length, 20)

    # def test_news_slug_max_length(self):
    #     max_length= self.test_news._meta.get_field('slug').max_length
    #     self.assertEqual(max_length, 200)

    def test_news_slug_creation(self):
        expected_slug = 'test-title'
        self.assertEqual(self.test_news.slug, expected_slug)

    def test_news_object_name(self):
        expected_object_name = self.test_news.title[0:30]
        self.assertEqual(str(self.test_news), expected_object_name)

    def test_news_get_absolute_url(self):
        expected_url = '/news/1/'
        self.assertEqual(self.test_news.get_absolute_url(), expected_url)

    def test_news_if_publish_creates_notifications(self):
        self.assertEqual(self.test_news.notification_set.count(), 0)
        self.test_news.publish()
        self.test_news.refresh_from_db()
        self.assertEqual(self.test_news.notification_set.count(), 1)

    def test_news_if_publish_creates_notification_flags(self):
        self.test_news.publish()
        self.test_news.refresh_from_db()
        notification = Notification.objects.get(pk=1)
        notification.refresh_from_db()
        self.assertEqual(notification.notificationreadflag_set.count(), 1)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class NewsFileModelTest(TestCase):
    # file
    # miniature
    # extension
    # isnews
    # objects
    # target_departament
    # target_location
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

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
        simple_file = SimpleUploadedFile(
            'testfile1.pdf', b'these are the file contents!')
        cls.test_news_file = NewsFile.objects.save_file(simple_file)
        cls.test_news_file.save()

        test_image_path = settings.MEDIA_DIR + '/test_image/dino.jpg'
        simple_file_image = SimpleUploadedFile(name='testimage.jpg',  content=open(
            test_image_path, 'rb').read(), content_type='image/jpeg')
        cls.test_news_file_2 = NewsFile.objects.save_file(simple_file_image)
        cls.test_news_file_2.save()

    def test_news_file_file_label(self):
        field_label = self.test_news_file._meta.get_field('file').verbose_name
        self.assertEqual(field_label, 'file')

    def test_news_file_extension_label(self):
        field_label = self.test_news_file._meta.get_field(
            'extension').verbose_name
        self.assertEqual(field_label, 'extension')

    def test_news_file_miniature_label(self):
        field_label = self.test_news_file._meta.get_field(
            'miniature').verbose_name
        self.assertEqual(field_label, 'miniature')

    def test_news_file_get_absolute_url(self):
        d = date.today()

        expected_url = '/media/upload/%s/%s/%s/%s' % (d.strftime('%Y'),
                                                      d.strftime('%m'), d.strftime('%d'), self.test_news_file)
        self.assertEqual(self.test_news_file.get_absolute_url(), expected_url)

    def test_news_file_object_name(self):
        expected_object_name = 'testfile1.pdf'
        expected_object_ext = '.pdf'
        self.assertEqual(self.test_news_file.file.name.split(
            '/')[-1], expected_object_name)
        self.assertEqual(self.test_news_file.file.name.split(
            '/')[-1][-4:], expected_object_ext)

    def test_news_file_extension_pdf(self):
        expected_object_ext = 'pdf'
        self.assertEqual(self.test_news_file.extension, expected_object_ext)

    def test_news_file_miniature_pdf(self):
        self.assertIsNone(self.test_news_file.miniature)

    def test_news_file_extension_image(self):
        expected_object_ext = 'image'
        self.assertEqual(self.test_news_file_2.extension, expected_object_ext)

    def test_news_file_miniature_path(self):
        expected_miniature_path = '/media/upload/thumbs/testimage-thumb.jpg'
        self.assertEqual(self.test_news_file_2.miniature,
                         expected_miniature_path)

    def test_news_file_miniature_size(self):
        expected_miniature_size = 128, 128
        miniature_path = settings.MEDIA_DIR + '/upload/thumbs/testimage-thumb.jpg'
        image = Image.open(miniature_path)
        self.assertEqual(image.size, expected_miniature_size)


class NotificationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

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
            author=test_user1,
        )
        cls.test_news.publish()
        cls.test_news.save()
        cls.test_notification = Notification.objects.get(pk=1)

    def test_notification_body_label(self):
        field_label = self.test_notification._meta.get_field(
            'body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_notification_title_label(self):
        field_label = self.test_notification._meta.get_field(
            'title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_notification_date_created_label(self):
        field_label = self.test_notification._meta.get_field(
            'date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_notification_body_max_length(self):
        max_length = self.test_notification._meta.get_field('body').max_length
        self.assertEqual(max_length, 1000)

    def test_notification_title_max_length(self):
        max_length = self.test_notification._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_news_object_name(self):
        expected_object_name = self.test_notification.body[0:20]
        self.assertEqual(str(self.test_notification), expected_object_name)


class NotificationReadFlagModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

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
            author=test_user1,
        )
        cls.test_news.publish()
        cls.test_news.save()
        cls.test_notificationreadflag = NotificationReadFlag.objects.get(pk=1)

    def test_notificationreadflag_read_label(self):
        field_label = self.test_notificationreadflag._meta.get_field(
            'read').verbose_name
        self.assertEqual(field_label, 'read')

    def test_notificationreadflag_user_label(self):
        field_label = self.test_notificationreadflag._meta.get_field(
            'user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_notificationreadflag_notification_label(self):
        field_label = self.test_notificationreadflag._meta.get_field(
            'notification').verbose_name
        self.assertEqual(field_label, 'notification')

    def test_notificationreadflag_object_name(self):
        expected_object_name = '{0} ({1}) '.format(
            self.test_notificationreadflag.user.userprofile, self.test_notificationreadflag.notification)
        self.assertEqual(str(self.test_notificationreadflag),
                         expected_object_name)


#
# class NewsReadFlagModelTest(TestCase):
#
#
#     @classmethod
#     def setUpTestData(cls):
#         test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
#
#         test_user1.save()
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
#         cls.test_news = News.objects.create(
#             title='test title',
#             body='test body',
#             author= test_user1,
#         )
#         cls.test_news.publish()
#         cls.test_news.save()
#         cls.test_newsreadflag = NewsReadFlag.objects.get(pk=1)
#
#     def test_newsreadflag_read_label(self):
#         field_label = self.test_newsreadflag._meta.get_field('read').verbose_name
#         self.assertEqual(field_label, 'read')
#
#     def test_newsreadflag_user_label(self):
#         field_label = self.test_newsreadflag._meta.get_field('user').verbose_name
#         self.assertEqual(field_label, 'user')
#
#     def test_newsreadflag_news_label(self):
#         field_label = self.test_newsreadflag._meta.get_field('news').verbose_name
#         self.assertEqual(field_label, 'news')
#
#     def test_newsreadflag_object_name(self):
#         expected_object_name = '{0} ({1}) '.format(self.test_newsreadflag.user.userprofile, self.test_newsreadflag.news)
#         self.assertEqual(str(self.test_newsreadflag), expected_object_name)
#
#


class KnowledgeCategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_category = KnowledgeCategory.objects.create(
            title='test category')

    def test_knowledgecategory_news_label(self):
        field_label = self.test_category._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_knowledgecategory_object_name(self):
        expected_object_name = self.test_category.title
        self.assertEqual(str(self.test_category), expected_object_name)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class DocFileModelTest(TestCase):
    # file
    # title
    # date_created
    # target_departament
    # target_location
    # category

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        cls.test_user1.save()
        cls.test_category = KnowledgeCategory.objects.create(
            title='test category')
        cls.test_file = SimpleUploadedFile('testfile.txt', b'test contents')
        cls.test_docfile = DocFile.objects.create(
            title='test title',
            file=cls.test_file,
            category=cls.test_category,
            author=cls.test_user1,
        )

    def test_docfile_title_label(self):
        field_label = self.test_docfile._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_docfile_date_created_label(self):
        field_label = self.test_docfile._meta.get_field(
            'date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_docfile_file_label(self):
        field_label = self.test_docfile._meta.get_field('file').verbose_name
        self.assertEqual(field_label, 'file')

    def test_docfile_target_departament_label(self):
        field_label = self.test_docfile._meta.get_field(
            'target_departament').verbose_name
        self.assertEqual(field_label, 'target departament')

    def test_docfile_target_location_label(self):
        field_label = self.test_docfile._meta.get_field(
            'target_location').verbose_name
        self.assertEqual(field_label, 'target location')

    def test_docfile_category_label(self):
        field_label = self.test_docfile._meta.get_field(
            'category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_docfile_title_max_length(self):
        max_length = self.test_docfile._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_docfile_target_location_max_length(self):
        max_length = self.test_docfile._meta.get_field(
            'target_location').max_length
        self.assertEqual(max_length, 3)

    def test_docfile_target_departament_max_length(self):
        max_length = self.test_docfile._meta.get_field(
            'target_departament').max_length
        self.assertEqual(max_length, 3)

    def test_docfile_object_name(self):
        expected_object_name = self.test_docfile.title
        self.assertEqual(str(self.test_docfile), expected_object_name)

    def test_docfile_get_absolute_url(self):
        d = date.today()

        expected_url = '/media/documents/%s/%s/%s/%s' % (d.strftime('%Y'),
                                                         d.strftime('%m'), d.strftime('%d'), self.test_file)
        self.assertEqual(self.test_docfile.get_absolute_url(), expected_url)


class DocumentFModelTest(TestCase):
    # title
    # body
    # author
    # date_created
    # target_departament
    # target_location
    # category
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

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
        cls.test_category = KnowledgeCategory.objects.create(
            title='test category')

        cls.test_documentf = DocumentF.objects.create(
            title='test title',
            body='test body',
            author=test_user1,
            category=cls.test_category,)

    def test_documentf_title_label(self):
        field_label = self.test_documentf._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_documentf_body_label(self):
        field_label = self.test_documentf._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_documentf_author_label(self):
        field_label = self.test_documentf._meta.get_field(
            'author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_documentf_date_created_label(self):
        field_label = self.test_documentf._meta.get_field(
            'date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_documentf_target_departament_label(self):
        field_label = self.test_documentf._meta.get_field(
            'target_departament').verbose_name
        self.assertEqual(field_label, 'target departament')

    def test_documentf_target_location_label(self):
        field_label = self.test_documentf._meta.get_field(
            'target_location').verbose_name
        self.assertEqual(field_label, 'target location')

    def test_documentf_category_label(self):
        field_label = self.test_documentf._meta.get_field(
            'category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_documentf_title_max_length(self):
        max_length = self.test_documentf._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_documentf_body_max_length(self):
        max_length = self.test_documentf._meta.get_field('body').max_length
        self.assertEqual(max_length, 5000)

    def test_documentf_target_location_max_length(self):
        max_length = self.test_documentf._meta.get_field(
            'target_location').max_length
        self.assertEqual(max_length, 3)

    def test_documentf_target_departament_max_length(self):
        max_length = self.test_documentf._meta.get_field(
            'target_departament').max_length
        self.assertEqual(max_length, 3)

    def test_documentf_object_name(self):
        expected_object_name = self.test_documentf.title
        self.assertEqual(str(self.test_documentf), expected_object_name)

    def test_documentf_get_absolute_url(self):
        expected_url = '/docs/1/'
        self.assertEqual(self.test_documentf.get_absolute_url(), expected_url)


class DocQuestionModelTest(TestCase):
    # title
    # body
    # author
    # date_created
    # target_departament
    # target_location
    # category
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

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
        cls.test_category = KnowledgeCategory.objects.create(
            title='test category')

        cls.test_docquestion = DocQuestion.objects.create(
            title='test title',
            body='test body',
            answer='test_answer',
            category=cls.test_category,)

    def test_docquestion_title_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_docquestion_body_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_docquestion_answer_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'answer').verbose_name
        self.assertEqual(field_label, 'answer')

    def test_docquestion_date_created_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'date_created').verbose_name
        self.assertEqual(field_label, 'date created')

    def test_docquestion_target_departament_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'target_departament').verbose_name
        self.assertEqual(field_label, 'target departament')

    def test_docquestion_target_location_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'target_location').verbose_name
        self.assertEqual(field_label, 'target location')

    def test_docquestion_category_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_docquestion_title_max_length(self):
        max_length = self.test_docquestion._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_docquestion_answer_max_length(self):
        max_length = self.test_docquestion._meta.get_field('answer').max_length
        self.assertEqual(max_length, 5000)

    def test_docquestion_body_max_length(self):
        max_length = self.test_docquestion._meta.get_field('body').max_length
        self.assertEqual(max_length, 5000)

    def test_docquestion_target_location_max_length(self):
        max_length = self.test_docquestion._meta.get_field(
            'target_location').max_length
        self.assertEqual(max_length, 3)

    def test_docquestion_target_departament_max_length(self):
        max_length = self.test_docquestion._meta.get_field(
            'target_departament').max_length
        self.assertEqual(max_length, 3)

    def test_docquestion_object_name(self):
        expected_object_name = self.test_docquestion.title
        self.assertEqual(str(self.test_docquestion), expected_object_name)


class UserQuestionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

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

        cls.test_docquestion = UserQuestion.objects.create(
            title='test title',
            body='test body',
            author=test_user1
        )

    def test_docquestion_title_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_docquestion_body_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_docquestion_author_label(self):
        field_label = self.test_docquestion._meta.get_field(
            'author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_docquestion_title_max_length(self):
        max_length = self.test_docquestion._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_docquestion_body_max_length(self):
        max_length = self.test_docquestion._meta.get_field('body').max_length
        self.assertEqual(max_length, 5000)

    def test_docquestion_object_name(self):
        expected_object_name = self.test_docquestion.title
        self.assertEqual(str(self.test_docquestion), expected_object_name)
