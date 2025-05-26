from django.apps import AppConfig

class WebsiteContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website_content'
    
    def ready(self):
        """Paleidžiama kai aplikacija pilnai įkrauta"""
        from .models import PageContent
        # Sukuriame trūkstamus puslapius aplikacijos paleidimo metu
        try:
            PageContent.ensure_all_pages_exist()
        except Exception:
            # Ignoruojame klaidas (pvz., jei duomenų bazė dar nesukurta)
            pass


# management/commands/create_pages.py (sukurkite šį failą)
# website_content/management/__init__.py (tuščias failas)
# website_content/management/commands/__init__.py (tuščias failas)
# website_content/management/commands/create_pages.py

from django.core.management.base import BaseCommand
from website_content.models import PageContent

class Command(BaseCommand):
    help = 'Sukuria visus reikalingus puslapius'
    
    def handle(self, *args, **options):
        PageContent.ensure_all_pages_exist()
        self.stdout.write(
            self.style.SUCCESS('Sėkmingai sukurti visi reikalingi puslapiai')
        )