import threading
import time
import requests
import subprocess
import os
from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nfc_project'

    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":
            return 

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nfc_project'
