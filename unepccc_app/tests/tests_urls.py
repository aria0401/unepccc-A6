from django.test import TestCase
from django.urls import reverse, resolve
from unepccc_app.views import index_view, project_list, project_detail


class TestUrls(TestCase):

    def test_index_url(self):
        url = reverse('unepccc_app:index-view')
        print(url)
        self.assertEquals(resolve(url).func, index_view)

    def test_project_list_url(self):
        url = reverse('unepccc_app:project-view')
        print(url)
        self.assertEquals(resolve(url).func, project_list)

    def test_project_detail_url(self):
        url = reverse('unepccc_app:project-details', args=[1])
        print(url)
        self.assertEquals(resolve(url).func, project_detail)
