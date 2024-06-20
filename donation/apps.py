from django.apps import AppConfig


class DonationConfig(AppConfig):
    """
    The DonationConfig class inherits from Django's AppConfig class.
    This class is used to configure the 'donation' application.

    Attributes:
        default_auto_field: A string representing the default auto field type
        to use for auto-created primary keys.
        name: A string representing the name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donation'
