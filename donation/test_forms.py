from django.test import TestCase

from .forms import DonationForm


class TestDonationForm(TestCase):
    def test_form_is_not_valid(self):
        form = DonationForm({'title': 'test'})
        self.assertFalse(form.is_valid(), msg="Form is not valid")

    def test_form_is_valid(self):
        form = DonationForm({'title': 'test',
                             'description': 'test description', 'goal': 100})
        self.assertTrue(form.is_valid(), msg="Form should be valid")

    def test_form_is_not_valid_without_title(self):
        form = DonationForm({'description': 'test description', 'goal': 100})
        self.assertFalse(form.is_valid(),
                         msg="Form should not be valid without title")

    def test_form_is_not_valid_without_goal(self):
        form = DonationForm(
            {'title': 'test', 'description': 'test description'})
        self.assertFalse(form.is_valid(),
                         msg="Form should not be valid without goal")

    def test_form_is_not_valid_with_invalid_goal(self):
        form = DonationForm({'title': 'test',
                             'description': 'test description',
                             'goal': 'invalid'})
        self.assertFalse(form.is_valid(),
                         msg="Form should not be valid with invalid goal")
