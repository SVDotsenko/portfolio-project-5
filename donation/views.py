import os
from itertools import cycle

from django.conf import settings
from django.contrib.auth.decorators import login_required
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
                           or 0)
        donation.percentage = donation.raised / donation.goal * 100

    context = {
        'donations': donations
    }
    return render(request, 'donation/donations.html', context)


@login_required
def redirect_to_donate(request, donation_id):
    context = {
        'donation_id': donation_id,
        'donations': Donation.objects.all(),
        'stripe_public_key': settings.STRIPE_PK
    }
    return render(request, 'donate/donate.html', context)


def history(request):
    context = {
        'payments': Payment.objects.all().values(
            'id',
            'user__username',
            'donation__title',
            'stripe_payment__amount',
            'stripe_payment__timestamp',
            'stripe_payment__stripe_charge_id'
        )
    }
    return render(request, 'donation/history.html', context)


def form(request):
    return render(request, 'donation/form.html')
