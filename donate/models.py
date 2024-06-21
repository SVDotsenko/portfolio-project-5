from django.contrib.auth.models import User
from django.db import models

from donation.models import Donation


class StripeTransaction(models.Model):
    """
    The StripeTransaction model represents a transaction made via Stripe.

    Attributes:
        stripe_charge_id: A CharField that stores the unique ID of the Stripe
        charge.
        amount: An IntegerField that stores the amount of the transaction.
        timestamp: A DateTimeField that stores the date and time the
        transaction was created. It is set to the current date/time by default.
    """
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    """
    The Payment model represents a payment made by a user.

    Attributes:
        user: A ForeignKey that links to the User model.
              It represents the user who made the payment.
        donation: A ForeignKey that links to the Donation model.
                   It represents the donation that the payment is associated
                   with.
        stripe_payment: A OneToOneField that links to the StripeTransaction
        model.
                        It represents the Stripe transaction associated with
                        the payment.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    stripe_payment = models.OneToOneField(StripeTransaction,
                                          on_delete=models.CASCADE)
