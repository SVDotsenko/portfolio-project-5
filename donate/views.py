from django.conf import settings
from django.shortcuts import redirect, render
import stripe


def donate(request):
    if request.method == 'POST':
        custom_amount = request.POST.get('custom-amount')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')

        stripe.api_key = settings.STRIPE_SK
        intent = stripe.PaymentIntent.create(
            amount=round(int(custom_amount) * 100),
            currency=settings.STRIPE_CURRENCY,
        )

        print('Custom Amount:', custom_amount)
        print('First Name:', first_name)
        print('Last Name:', last_name)
        print('Email:', email)

        template = 'donate/donate.html'
        context = {
            'stripe_public_key': settings.STRIPE_PK,
            'client_secret': intent.client_secret,
        }
        return render(request, template, context)

    return redirect('donations')
