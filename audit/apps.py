from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit'
    verbose_name = 'Audit Log'

    def ready(self):
        # Import signal handlers so audit events are registered when the app is ready.
        from . import signals  # noqa: F401
