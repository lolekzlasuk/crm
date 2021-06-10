from django.test import SimpleTestCase
from django.urls import reverse, resolve
from calendary.views import DeventDetailView, CalListView, post_devent


class TestUrls(SimpleTestCase):

    def test_DeventDetailView_url_resolves(self):
        url = reverse('calendary:devent',args=['12'])
        self.assertEquals(resolve(url).func.view_class, DeventDetailView)

    def test_CalListView_resolves(self):
        url = reverse('calendary:calendary',args=['12','10'])
        self.assertEquals(resolve(url).func.view_class, CalListView)

    def test_post_devent_resolves(self):
        url = reverse('calendary:post_devent',args=['12'])
        self.assertEquals(resolve(url).func, post_devent)
