from django.urls import path
from donation import views

urlpatterns = [
    path('donate/<int:donation_id>', views.redirect_to_donate,
         name='redirect_to_donate'),
    path('history/', views.history, name='history'),
]
