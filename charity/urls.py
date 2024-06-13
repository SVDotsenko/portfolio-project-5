"""
URL configuration for charity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found as default_page_not_found

from donation.views import donations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', donations, name='donations'),
    path('', include('donation.urls')),
    path('donat/', include('donate.urls')),
    path('accounts/', include('allauth.urls')),
]


def custom_page_not_found(request, exception):
    """
    Custom handler for page not found (404) errors.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that triggered the 404 error.

    Returns:
        HttpResponse: The response with the custom 404 page.
    """
    response = default_page_not_found(request, exception)
    response.template_name = '404.html'
    return response
