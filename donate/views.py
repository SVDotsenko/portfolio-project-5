import stripe
from django.conf import settings
from django.shortcuts import redirect


def donate(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SK
        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['first-name'],
            source=request.POST['stripeToken']
        )

        stripe.Charge.create(
            customer=customer,
            amount=int(request.POST['custom-amount']) * 100,
            currency='usd',
            description="Donation"
        )

    return redirect('donations')
