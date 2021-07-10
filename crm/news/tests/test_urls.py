# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from calendary import views
#
#
# class TestUrls(SimpleTestCase):
#
#     def test_KnowledgeCategoryListView_url_resolves(self):
#         url = reverse('news:knowledge',args=[])
#         self.assertEquals(resolve(url).func.view_class, KnowledgeCategoryListView)
#
#     def test_KnowledgeCategoryDetailView_url_resolves(self):
#         url = reverse('news:knowledgedetail',args=['1'])
#         self.assertEquals(resolve(url).func.view_class, KnowledgeCategoryDetailView)
#
#     def test_QuestionListView_url_resolves(self):
#         url = reverse('news:faq',args=[])
#         self.assertEquals(resolve(url).func.view_class, QuestionListView)
#
#     def test_UnansweredQuestionListView_url_resolves(self):
#         url = reverse('news:pending_faq',args=[])
#         self.assertEquals(resolve(url).func.view_class, UnansweredQuestionListView)
#
#     def test_UnpublishedNewsListView_url_resolves(self):
#         url = reverse('news:unpublished',args=[])
#         self.assertEquals(resolve(url).func.view_class, UnpublishedNewsListView)
#
#     def test_NewsDetailView_url_resolves(self):
#         url = reverse('news:newsdetail',args=['1'])
#         self.assertEquals(resolve(url).func.view_class, NewsDetailView)
#
#     def test_DocDetailView_url_resolves(self):
#         url = reverse('news:docdetail',args=['1'])
#         self.assertEquals(resolve(url).func.view_class, DocDetailView)
#
#     def test_NewsListView_url_resolves(self):
#         url = reverse('news:news_list',args=[])
#         self.assertEquals(resolve(url).func.view_class, NewsListView)
#
#     def test_post_news_url_resolves(self):
#         url = reverse('news:post_news',args=[])
#         self.assertEquals(resolve(url).func, post_news)
#
#     def test_publish_news_url_resolves(self):
#         url = reverse('news:publish_news',args=['1'])
#         self.assertEquals(resolve(url).func, publish_news)
#
#     def test_answer_question_url_resolves(self):
#         url = reverse('news:answerfaq',args=['1'])
#         self.assertEquals(resolve(url).func, answer_question)
#
#     def test_flagtoggle_url_resolves(self):
#         url = reverse('news:flagtoggle',args=[])
#         self.assertEquals(resolve(url).func, flagtoggle_url)
#
#     # def test_newsreadflagtoggle_url_resolves(self):
#     #     url = reverse('news:newsreadflag',args=[])
#     #     self.assertEquals(resolve(url).func, newsreadflagtoggle)
#
#     def test_markall_url_resolves(self):
#         url = reverse('news:markall',args=[])
#         self.assertEquals(resolve(url).func, markall_url)
#
#     def test_post_document_url_resolves(self):
#         url = reverse('news:post_document',args=[])
#         self.assertEquals(resolve(url).func, post_document)
#
#     def test_post_file_url_resolves(self):
#         url = reverse('news:post_file',args=[])
#         self.assertEquals(resolve(url).func, post_file)
#
#     def test_post_question_url_resolves(self):
#         url = reverse('news:post_question',args=[])
#         self.assertEquals(resolve(url).func, post_question)
#
#     def test_post_userquestion_url_resolves(self):
#         url = reverse('news:post_userquestion',args=[])
#         self.assertEquals(resolve(url).func, post_userquestion)
