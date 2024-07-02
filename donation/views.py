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
    """
    Calculate the total amount raised for a given donation.

    Args:
        donation: The donation object for which to calculate the total amount
        raised.

    Returns:
        The total amount raised for the donation. If no payments are found,
        returns 0.
    """
    return (Payment.objects.filter(donation=donation)
            .aggregate(Sum('stripe_payment__amount'))
            ['stripe_payment__amount__sum'] or 0)


def donations(request):
    """
    View function that retrieves a list of donations, assigns images to each
    donation, calculates the raised amount and percentage for each donation,
    and renders the 'donation/donations.html' template with the sorted list of
    donations.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template
    """
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
    """
    Redirects the user to the donate page if they are not a superuser.
    If the user is a superuser, it redirects them to the donations page.

    Args:
        request (HttpRequest): The HTTP request object.
        donation_id (int): The ID of the donation.

    Returns:
        HttpResponse: The rendered donate page or the donations page.

    """
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
    """
    View function that displays the donation history.

    Retrieves the list of donors and their total donation amounts,
    as well as the list of payments made, and paginates the results.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template
    """
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

    paginator = Paginator(payments_list, 12)

    page_number = request.GET.get('page')
    payments = paginator.get_page(page_number)

    context = {
        'payments': payments,
        'donors': donors,
        'total_donation': total_donation,
    }
    return render(request, 'donation/history.html', context)


class AdminRequiredMixin(UserPassesTestMixin):
    """
    A mixin class that requires the user to be a superuser.

    This mixin is used to restrict access to views or class-based views
    that should only be accessible by superusers. It checks if the user
    is a superuser by calling the `test_func` method.

    If the user is not a superuser, it displays an error message and
    redirects the user to the 'donations' page.
    """

    def test_func(self):
        """
        Checks if the user is a superuser.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Handles the case when a user does not have permission to access a page.

        Displays an error message to the user and redirects them to the
        donations page.
        """
        messages.error(self.request, 'You are not allowed to access this page')
        return redirect('donations')


class DonationCard(AdminRequiredMixin, View):
    """
    A class-based view for handling donation cards.

    This view allows users to create and update donation cards.

    Attributes:
        - AdminRequiredMixin: A mixin that requires the user to be an admin.
        - View: The base class for all views.

    Methods:
        - get: Handles GET requests for creating or updating a donation card.
        - post: Handles POST requests for creating or updating a donation card.
    """

    def get(self, request, donation_id=-1):
        """
        Handles the GET request for the donation form.

        If a donation_id is provided, it retrieves the corresponding
        Donation object
        from the database and renders the donation form template with the
        donation data.
        If no donation_id is provided, it simply renders the donation form
        template.

        Args:
            request (HttpRequest): The HTTP request object.
            donation_id (int, optional): The ID of the donation object to
            retrieve. Defaults to -1.

        Returns:
            HttpResponse: The HTTP response object containing the rendered
            template.
        """
        if donation_id < 0:
            return render(request, 'donation/form.html')

        return render(request, 'donation/form.html',
                      {'donation': Donation.objects.get(id=donation_id)})

    def post(self, request, donation_id=-1):
        """
        Handle the HTTP POST request for creating or updating a donation.

        Args:
            request (HttpRequest): The HTTP request object.
            donation_id (int, optional): The ID of the donation to be updated.
            Defaults to -1.

        Returns:
            HttpResponseRedirect: A redirect response to the 'donations' page.

        Raises:
            Http404: If the donation with the specified ID does not exist.

        """
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
    """
    Deletes a donation object from the database.

    Args:
        request (HttpRequest): The HTTP request object.
        donation_id (int): The ID of the donation to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the 'donations' page.

    Raises:
        Http404: If the donation with the specified ID does not exist.
    """
    donation = get_object_or_404(Donation, id=donation_id)
    if request.user.is_superuser:
        if raised(donation) > 0:
            messages.error(request, 'Card cannot be deleted because donations '
                                    'have already been made to it')
            return redirect('donations')
        donation.delete()
        message = (f'Donation {donation.title.capitalize()} deleted '
                   f'successfully')
        messages.success(request, message)
    else:
        messages.error(request, 'You are not allowed to access this page')

    return redirect('donations')
