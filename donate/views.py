import stripe
from django.conf import settings
from django.contrib.auth import get_user
from django.shortcuts import redirect
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
            amount=charge['amount'],
        )
    )


def make_stripe_payment(request):
    stripe.api_key = settings.STRIPE_SK
    user = get_user(request)
    customer = stripe.Customer.create(
        email=user.email,
        name=user.first_name,
        source=request.POST['stripeToken']
    )

    return stripe.Charge.create(
        customer=customer,
        amount=int(request.POST['custom-amount']) * 100,
        currency='usd',
        description=Donation.objects.get(id=request.POST['cause']).title
    )


def donate(request):
    if request.method == 'POST':
        update_user_details(request)
        charge = make_stripe_payment(request)
        save_transaction(request, charge)

    return redirect('donations')
