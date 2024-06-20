from django import forms
from .models import Donation


class DonationForm(forms.ModelForm):
    """
    A form for creating or updating a donation.

    This form is used to create or update a donation object. It is based on the
     Donation model
    and includes fields for the title, description, and goal of the donation.

    Attributes:
        model (Donation): The Donation model that this form is based on.
        fields (list): The fields from the model that should be included in the
         form.

    """
    class Meta:
        model = Donation
        fields = ['title', 'description', 'goal']
