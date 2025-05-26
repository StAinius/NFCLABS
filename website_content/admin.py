from django.contrib import admin
from django.db import models
from .models import PageContent
from tinymce.widgets import TinyMCE
from django.conf import settings

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('get_display_name', 'title', 'updated_at')
    search_fields = ('content',)
    readonly_fields = ('page_key',)
    
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30},
                                          mce_attrs=settings.TINYMCE_DEFAULT_CONFIG)},
    }
    
    def get_display_name(self, obj):
        return obj.get_display_name()
    get_display_name.short_description = 'Website'
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False  # Neleidžiame rankinio pridėjimo
    
    def changelist_view(self, request, extra_context=None):
        """Automatiškai sukuriame trūkstamus puslapius prieš rodant sąrašą"""
        PageContent.ensure_all_pages_exist()
        return super().changelist_view(request, extra_context)