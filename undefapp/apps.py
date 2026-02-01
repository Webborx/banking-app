from django.apps import AppConfig


class UndefappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'undefapp'

    def ready(self):
        from . import signals
