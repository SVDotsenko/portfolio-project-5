from django.apps import AppConfig


class DonateConfig(AppConfig):
    """
    The DonateConfig class inherits from Django's AppConfig class.
    This class is used to configure the 'donate' application.

    Attributes:
        default_auto_field: A string representing the default auto field type
        to use for auto-created primary keys.
        name: A string representing the name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donate'
