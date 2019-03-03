from django.apps import AppConfig


class RestapiConfig(AppConfig):
    name = 'geo_django_rf.restapi'

    def ready(self):
        # import signal handlers
        import geo_django_rf.restapi.signals
