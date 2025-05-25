from django.db import models
from django.contrib import admin
from tinymce.widgets import TinyMCE
from django import forms

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
    
    class Meta:
        verbose_name = "Website Content"
        verbose_name_plural = "Websites Content"

# Admin class with TinyMCE widget
@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ['get_display_name', 'title', 'updated_at']
    list_filter = ['page_key', 'updated_at']
    search_fields = ['title', 'content']
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'plugins': 'link image preview code table lists'}
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)
