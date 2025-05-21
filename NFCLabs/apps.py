import os
from django.apps import AppConfig


class NFCLabsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "NFCLabs"

    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":
            return
