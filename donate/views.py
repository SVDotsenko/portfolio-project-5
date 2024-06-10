import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user
from django.shortcuts import redirect
from stripe.error import StripeError

from donate.models import StripeTransaction, Payment
from donation.models import Donation


def update_user_details(request):
    user = get_user(request)
    user.first_name = request.POST['first-name']
    user.last_name = request.POST['last-name']
    user.email = request.POST['email']
    user.save()


def save_transaction(request, charge):
    Payment.objects.create(
        user=get_user(request),
        donation=Donation.objects.get(id=request.POST['cause']),
        stripe_payment=StripeTransaction.objects.create(
            stripe_charge_id=charge['id'],
            amount=charge['amount'] / 100,
        )
    )


def make_stripe_payment(request):
    stripe.api_key = settings.STRIPE_SK
    user = get_user(request)

    try:
        return stripe.Charge.create(
            amount=int(request.POST['custom-amount']) * 100,
            currency='usd',
            description=Donation.objects.get(id=request.POST['cause']).title,
            customer=stripe.Customer.create(
                email=user.email,
                name=user.username,
                source=request.POST['stripeToken']
            )
        )
    except StripeError as e:
        messages.add_message(request, messages.ERROR, str(e))
        return None


def donate(request):
    if request.method == 'POST':
        update_user_details(request)
        charge = make_stripe_payment(request)
        if charge is None:
            return redirect('donations')
        save_transaction(request, charge)
        message = (f'Thank you for your donation of '
                   f'${int(charge["amount"] / 100)}, You may see it in '
                   f'the first row of this table')
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('history')
