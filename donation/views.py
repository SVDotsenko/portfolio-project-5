import os
from itertools import cycle

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
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
        'donations': sorted(donations, key=lambda d: d.raised - d.goal)
    }
    return render(request, 'donation/donations.html', context)


@login_required
def redirect_to_donate(request, donation_id):
    if request.user.is_superuser:
        return redirect('donations')

    donations = Donation.objects.all()
    for donation in donations:
        donation.raised = raised(donation)

    context = {
        'donation_id': donation_id,
        'donations': [donation for donation in donations if
                      donation.raised < donation.goal],
        'stripe_public_key': settings.STRIPE_PK
    }
    return render(request, 'donate/donate.html', context)


def history(request):
    donors = (User.objects.annotate(
        amount=Coalesce(Sum('payment__stripe_payment__amount'), Value(0)))
              .values('username', 'amount')
              .order_by('-amount'))

    total_donation = sum(donor['amount'] for donor in donors)

    payments_list = Payment.objects.all().values(
        'id',
        'user__username',
        'donation__title',
        'stripe_payment__amount',
        'stripe_payment__timestamp',
        'stripe_payment__stripe_charge_id'
    ).order_by('-stripe_payment__timestamp')

    paginator = Paginator(payments_list, 10)

    page_number = request.GET.get('page')
    payments = paginator.get_page(page_number)

    context = {
        'payments': payments,
        'donors': donors,
        'total_donation': total_donation,
    }
    return render(request, 'donation/history.html', context)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request,
                       'You are not allowed to access to this page')
        return redirect('donations')


class DonationCard(AdminRequiredMixin, View):
    def get(self, request, donation_id=-1):
        if donation_id < 0:
            return render(request, 'donation/form.html')

        return render(request, 'donation/form.html',
                      {'donation': Donation.objects.get(id=donation_id)})

    def post(self, request, donation_id=-1):
        if donation_id < 0:
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                title = donation_form.cleaned_data.get('title', '')
                message = f'Donation {title.capitalize()} created successfully'
                donation_form.save()
                messages.success(request, message)
                return redirect('donations')

        donation = get_object_or_404(Donation, id=donation_id)
        donation_form = DonationForm(request.POST, instance=donation)
        if donation_form.is_valid():
            title = donation_form.cleaned_data.get('title', '')
            message = f'Donation {title.capitalize()} updated successfully'
            donation_form.save()
            messages.success(request, message)
            return redirect('donations')

        messages.error(request, donation_form.errors)


def delete_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donation.delete()
    message = f'Donation {donation.title.capitalize()} deleted successfully'
    messages.success(request, message)
    return redirect('donations')
