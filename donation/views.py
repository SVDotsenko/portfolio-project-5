from django.http import HttpResponse


# Create your views here.
def my_donation(request):
    return HttpResponse("Hello, Charity!")
