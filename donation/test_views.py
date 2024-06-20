from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from donation.models import Donation


class DonationViewTests(TestCase):
    def setUp(self):
        """
        Set up the necessary objects and data for the test case.

        This method is called before each test method is executed. It creates
        a superuser object with the username 'superuser' and password '12345'.
        It also creates a Donation object with the title 'Test Donation', goal
        of 1000, and description 'Test Description'.

        """
        self.user = User.objects.create_superuser(username='superuser',
                                                  password='12345')
        self.donation = Donation(title='Test Donation',
                                 goal=1000, description='Test Description')
        self.donation.save()

    def test_delete_donation(self):
        """
        Test case to verify the deletion of a donation.

        This test logs in a user with the username 'superuser' and password
        '12345'.
        It then checks the initial count of Donation objects in the database.
        Next, it sends a POST request to the 'delete_donation' view with the
        donation_id as a parameter.
        Finally, it asserts that the count of Donation objects in the database
        is now zero, indicating successful deletion.
        """
        self.client.login(username='superuser', password='12345')
        self.assertEqual(Donation.objects.count(), 1)
        self.client.post(reverse('delete_donation',
                                 kwargs={'donation_id': self.donation.id}))
        self.assertEqual(Donation.objects.count(), 0)

    def test_render_donations_page_not_superuser(self):
        """
        Test case to verify that the donations page is rendered correctly for
        a non-superuser.

        It checks that the HTTP response status code is 200, and that the
        content of the response
        contains the text "Donate now" but does not contain the texts "Edit"
        and "Delete".
        """
        response = self.client.get(reverse('donations'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Donate now", response.content)
        self.assertNotIn(b"Edit", response.content)
        self.assertNotIn(b"Delete", response.content)

    def test_render_donations_page_superuser(self):
        """
        Test case to verify the rendering of the donations page for a superuser

        This test logs in a superuser, makes a GET request to the 'donations'
        URL,
        and asserts that the response status code is 200 (OK). It also checks
        that
        the response content contains the strings "Edit" and "Delete", but
        does not
        contain the string "Donate now".

        """
        self.client.login(username='superuser', password='12345')
        response = self.client.get(reverse('donations'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit", response.content)
        self.assertIn(b"Delete", response.content)
        self.assertNotIn(b"Donate now", response.content)

    def test_render_history_page(self):
        """
        Test case to verify the rendering of the history page.

        It sends a GET request to the 'history' URL and checks if the response
        status code is 200. It also checks if certain content is present in the
        response content, including 'Payment', 'ID', 'Stripe Charge ID',
        'Username',
        'Donation', 'Title', 'Amount', 'Timestamp', and 'Total'.

        This test ensures that the history page is rendered correctly and
        contains
        the expected content.

        """
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Payment", response.content)
        self.assertIn(b"ID", response.content)
        self.assertIn(b"Stripe Charge ID", response.content)
        self.assertIn(b"Username", response.content)
        self.assertIn(b"Donation", response.content)
        self.assertIn(b"Title", response.content)
        self.assertIn(b"Amount", response.content)
        self.assertIn(b"Timestamp", response.content)
        self.assertIn(b"Total", response.content)

    def test_redirect_to_donate_login(self):
        """
        Test case to verify that a user is redirected to the donate page after
        logging in.
        """
        self.user = User.objects.create_user(username='user', password='12345')
        self.client.login(username='user', password='12345')
        response = self.client.get(reverse('redirect_to_donate',
                                           kwargs={
                                               'donation_id': self.donation.id
                                           }), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You may change a cause", response.content)

    def test_redirect_to_donate_not_login(self):
        """
        Test case to verify that a user who is not logged in is redirected to
        the donate page.

        This test sends a GET request to the 'redirect_to_donate' view with the
         donation ID as a parameter.
        It then checks that the response status code is 200 (OK) and that the
        content does not contain the
        message "You may change a cause".

        """
        response = self.client.get(reverse('redirect_to_donate',
                                           kwargs={
                                               'donation_id': self.donation.id
                                           }), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"You may change a cause", response.content)

    def test_create_donation(self):
        """
        Test case to verify the creation of a donation.

        This test logs in a superuser, creates a donation using the
        'create_donation' view,
        and then checks if the number of donations in the database has
        increased by 1.

        """
        self.client.login(username='superuser', password='12345')
        post_data = {
            'title': 'Test Donation2',
            'goal': 2000,
            'description': 'Test Description2'
        }
        self.assertEqual(Donation.objects.count(), 1)
        self.client.post(reverse('create_donation'), post_data)
        self.assertEqual(Donation.objects.count(), 2)

    def test_update_donation(self):
        """
        Test case for updating a donation.

        This method tests the functionality of updating a donation by sending
        a POST request to the 'update_donation'
        view with the necessary data. It then checks if the donation object
        has been updated correctly by asserting
        the expected values against the actual values.

        Steps:
        1. Log in as a superuser.
        2. Create a dictionary containing the updated donation data.
        3. Send a POST request to the 'update_donation' view with the donation
        ID and the updated data.
        4. Refresh the donation object from the database.
        5. Assert that the updated values match the expected values.

        """
        self.client.login(username='superuser', password='12345')
        post_data = {
            'title': 'Test Donation2',
            'goal': 2000,
            'description': 'Test Description2'
        }
        self.client.post(reverse('update_donation',
                                 kwargs={'donation_id': self.donation.id}),
                         post_data)
        self.donation.refresh_from_db()
        self.assertEqual(self.donation.title, 'Test Donation2')
        self.assertEqual(self.donation.goal, 2000)
        self.assertEqual(self.donation.description, 'Test Description2')
