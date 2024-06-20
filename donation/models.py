from django.db import models


class Donation(models.Model):
    """
    The Donation class inherits from Django's Model class.
    This class represents a donation in the application.

    Attributes:
        title: A CharField representing the title of the donation. Maximum
        length is 200 characters.
        description: A TextField representing the description of the donation.
        goal: An IntegerField representing the goal amount for the donation.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
