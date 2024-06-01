from django.contrib.auth.models import User
from django.db import models

from donation.models import Donation


class StripeTransaction(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    stripe_payment = models.OneToOneField(StripeTransaction,
                                          on_delete=models.CASCADE)
