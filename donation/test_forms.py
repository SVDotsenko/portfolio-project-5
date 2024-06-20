from django.test import TestCase

from .forms import DonationForm


class TestDonationForm(TestCase):
    def test_form_is_not_valid(self):
        """
        Test case to check if the DonationForm is not valid when 'title' field
        is provided with a value.
        """
        form = DonationForm({'title': 'test'})
        self.assertFalse(form.is_valid(), msg="Form is not valid")

    def test_form_is_valid(self):
        """
        Test case to check if the DonationForm is valid.

        This test case creates an instance of the DonationForm with some test
        data and
        checks if the form is valid using the `is_valid()` method. It asserts
        that the
        form should be valid.

        """
        form = DonationForm({'title': 'test',
                             'description': 'test description', 'goal': 100})
        self.assertTrue(form.is_valid(), msg="Form should be valid")

    def test_form_is_not_valid_without_title(self):
        """
        Test case to check if the form is not valid without a title.

        The form is initialized with a description and a goal, but without a
        title.
        The test asserts that the form should not be valid without a title.
        """
        form = DonationForm({'description': 'test description', 'goal': 100})
        self.assertFalse(form.is_valid(),
                         msg="Form should not be valid without title")

    def test_form_is_not_valid_without_goal(self):
        """
        Test case to check if the form is not valid without a goal.

        The form is initialized with a title and description, but without a
        goal.
        The test asserts that the form should not be valid without a goal.
        """
        form = DonationForm(
            {'title': 'test', 'description': 'test description'})
        self.assertFalse(form.is_valid(),
                         msg="Form should not be valid without goal")

    def test_form_is_not_valid_with_invalid_goal(self):
        """
        Test case to check if the form is not valid when an invalid goal is
        provided.

        The test creates a DonationForm instance with an invalid goal value and
         checks if the form is not valid.
        The goal value is set to 'invalid' to simulate an invalid input.
        The test asserts that the form should not be valid with an invalid goal

        """
        form = DonationForm({'title': 'test',
                             'description': 'test description',
                             'goal': 'invalid'})
        self.assertFalse(form.is_valid(),
                         msg="Form should not be valid with invalid goal")
