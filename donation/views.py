import os
from itertools import cycle

from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render

from donate.models import Payment
from donation.models import Donation


def donations(request):
    IMAGE_DIR = 'static/images/causes'
    image_cycle = cycle(os.listdir(IMAGE_DIR))
    donations = Donation.objects.all()
    for donation in donations:
        donation.image = IMAGE_DIR + '/' + next(image_cycle)
        donation.raised = (Payment.objects.filter(donation=donation).aggregate(
            Sum('stripe_payment__amount'))['stripe_payment__amount__sum']
                           or 0) / 100
        donation.percentage = donation.raised / donation.goal * 100

    context = {
        'donations': donations
    }
    return render(request, 'donation/donations.html', context)


def redirect_to_donate(request, donation_id):
    context = {
        'donation_id': donation_id,
        'donations': Donation.objects.all(),
        'stripe_public_key': settings.STRIPE_PK
    }
    return render(request, 'donate/donate.html', context)
