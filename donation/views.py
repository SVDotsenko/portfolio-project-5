import os
import random

from django.shortcuts import render


def donations(request):
    images = os.listdir('static/images/causes')
    donations = [
        {
            'image': 'static/images/causes/' + random.choice(images),
            'title': "Title 1",
            'description': "Description 1",
            'raised': 30000,
            'goal': 50000,
        },
        {
            'image': 'static/images/causes/' + random.choice(images),
            'title': "Title 2",
            'description': "Description 2",
            'raised': 60000,
            'goal': 70000,
        },
        {
            'image': 'static/images/causes/' + random.choice(images),
            'title': "Title 3",
            'description': "Description 3",
            'raised': 80000,
            'goal': 100000,
        },
    ]
    return render(request, 'donation/donations.html', {'donations': donations})
