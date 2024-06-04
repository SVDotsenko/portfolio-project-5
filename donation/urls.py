from django.urls import path
from donation import views
from donation.views import DonationCard

urlpatterns = [
    path('donate/<int:donation_id>', views.redirect_to_donate,
         name='redirect_to_donate'),
    path('history/', views.history, name='history'),
    path('create/', DonationCard.as_view(), name='create_donation'),
]
