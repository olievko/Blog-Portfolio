from django.test import TestCase
# Create your tests here.

from projects.forms import ContactForm


class ContactFormTest(TestCase):
    # Valid Form Data
    def test_ContactForm_valid(self):
        form = ContactForm(data={
            "contact_name": "user",
            "contact_email": "user@gmail.com",
            "subject": "subject",
            "message": "Hello World!",
        })
        self.assertTrue(form.is_valid())

        # Invalid Form Data
    def test_ContactForm_invalid(self):
        form = ContactForm(data={
            'contact_name': "name",
            'contact_email': "name",
            "subject": "",
            "message": "Hello World!",
        })
        self.assertFalse(form.is_valid())