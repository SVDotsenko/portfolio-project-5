import os
from itertools import cycle

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from donate.models import Payment
from donation.forms import DonationForm
from donation.models import Donation


def raised(donation):
    return (Payment.objects.filter(donation=donation)
            .aggregate(Sum('stripe_payment__amount'))
            ['stripe_payment__amount__sum'] or 0)


def donations(request):
    IMAGE_DIR = 'static/images/causes'
    image_cycle = cycle(os.listdir(IMAGE_DIR))
    donations = Donation.objects.all()
    for donation in donations:
        donation.image = IMAGE_DIR + '/' + next(image_cycle)
        donation.raised = raised(donation)
        donation.percentage = donation.raised / donation.goal * 100

    context = {
        'donations': sorted(donations, key=lambda d: d.goal - d.raised,
                            reverse=True)
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


class DonationCard(View):
    def get(self, request, donation_id=-1):
        if donation_id < 0:
            return render(request, 'donation/form.html')

        return render(request, 'donation/form.html',
                      {'donation': Donation.objects.get(id=donation_id)})

    def post(self, request, donation_id=-1):
        if donation_id < 0:
            donation_form = DonationForm(request.POST)
        else:
            donation = get_object_or_404(Donation, id=donation_id)
            donation_form = DonationForm(request.POST, instance=donation)

        if donation_form.is_valid():
            donation_form.save()
            return redirect('donations')

        print(donation_form.errors)
