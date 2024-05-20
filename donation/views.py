from django.shortcuts import render


def donations(request):
    return render(request, 'donation/donations.html')
