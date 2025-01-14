from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    def ready(self):
        """
        Imports the signals for the payment app when the application starts.
        """
        import payment.signals
