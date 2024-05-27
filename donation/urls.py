from django.urls import path
from donation import views

urlpatterns = [
    path('<int:donation_id>', views.redirect_to_donate,
         name="redirect_to_donate"),
]
