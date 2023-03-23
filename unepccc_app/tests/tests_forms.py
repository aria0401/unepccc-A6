from django.test import TestCase
from unepccc_app.forms import ProjectForm


class TestForms(TestCase):

    def test_project_form(self):
        form = ProjectForm(data={
            'name': 'test name'
        })
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['name'], 'test name')

    def test_project_form_no_data(self):
        form = ProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
