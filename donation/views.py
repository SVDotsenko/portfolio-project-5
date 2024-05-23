import os
from itertools import cycle
from django.shortcuts import render


def donations(request):
    image_cycle = cycle(os.listdir('static/images/causes'))
    donations = [
        {
            'image': 'static/images/causes/' + next(image_cycle),
            'title': "Title 1",
            'description': "Description 1",
            'raised': 30000,
            'goal': 50000,
        },
        {
            'image': 'static/images/causes/' + next(image_cycle),
            'title': "Title 2",
            'description': "Description 2",
            'raised': 60000,
            'goal': 70000,
        },
        {
            'image': 'static/images/causes/' + next(image_cycle),
            'title': "Title 3",
            'description': "Description 3",
            'raised': 80000,
            'goal': 100000,
        },
    ]

    for donation in donations:
        donation['percentage'] = donation['raised'] / donation['goal'] * 100

    return render(request, 'donation/donations.html', {'donations': donations})
