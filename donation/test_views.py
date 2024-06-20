from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from donation.models import Donation


class DonationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='superuser',
                                                  password='12345')
        self.donation = Donation(title='Test Donation',
                                 goal=1000, description='Test Description')
        self.donation.save()

    def test_delete_donation(self):
        self.client.login(username='superuser', password='12345')
        self.assertEqual(Donation.objects.count(), 1)
        self.client.post(reverse('delete_donation',
                                 kwargs={'donation_id': self.donation.id}))
        self.assertEqual(Donation.objects.count(), 0)

    def test_render_donations_page_not_superuser(self):
        response = self.client.get(reverse('donations'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Donate now", response.content)
        self.assertNotIn(b"Edit", response.content)
        self.assertNotIn(b"Delete", response.content)

    def test_render_donations_page_superuser(self):
        self.client.login(username='superuser', password='12345')
        response = self.client.get(reverse('donations'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit", response.content)
        self.assertIn(b"Delete", response.content)
        self.assertNotIn(b"Donate now", response.content)

    def test_render_history_page(self):
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
        self.user = User.objects.create_user(username='user', password='12345')
        self.client.login(username='user', password='12345')
        response = self.client.get(reverse('redirect_to_donate',
                                           kwargs={
                                               'donation_id': self.donation.id
                                           }), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You may change a cause", response.content)

    def test_redirect_to_donate_not_login(self):
        response = self.client.get(reverse('redirect_to_donate',
                                           kwargs={
                                               'donation_id': self.donation.id
                                           }), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"You may change a cause", response.content)

    def test_create_donation(self):
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