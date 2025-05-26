from django.db import models

class PageContent(models.Model):
    WEBSITES = {
        'about': 'About US',
        'products': 'Products',
        'solutions': 'Solutions',
        'home': 'Home',
        'contact': 'Contacts',
    }
    
    page_key = models.CharField(max_length=50, unique=True, verbose_name="Website")
    title = models.CharField(max_length=200, verbose_name="Name")
    content = models.TextField(verbose_name="Content")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta description")
    meta_keywords = models.CharField(max_length=200, blank=True, verbose_name="Meta keywords")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Data")
    
    def __str__(self):
        return self.WEBSITES.get(self.page_key, self.page_key)
    
    def get_display_name(self):
        return self.WEBSITES.get(self.page_key, self.page_key)
    
    @classmethod
    def ensure_all_pages_exist(cls):
        """Automatiškai sukuria trūkstamus puslapius"""
        for page_key, display_name in cls.WEBSITES.items():
            obj, created = cls.objects.get_or_create(
                page_key=page_key,
                defaults={
                    'title': display_name,
                    'content': f'<p>Turinys puslapiui: {display_name}</p>',
                    'meta_description': f'{display_name} page description',
                }
            )
            if created:
                print(f"Sukurtas puslapis: {display_name}")
    
    class Meta:
        verbose_name = "Website Content"
        verbose_name_plural = "Websites Content"
