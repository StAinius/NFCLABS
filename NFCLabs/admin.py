from django.contrib import admin
from django.db import models
from .models import Category, Product, ProductFile, Solution, ProductImage
from tinymce.widgets import TinyMCE
from django.conf import settings
from django import forms
from .models import ContactPage

class WebsiteContentAdminSite(admin.AdminSite):
    site_header = "NFCLabs turinys"
    site_title = "NFCLabs turinio administravimas"
    index_title = "Svetainės turinys"


content_admin_site = WebsiteContentAdminSite(name="content_admin")


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1
    max_num = 10


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "available", "updated"]
    list_filter = ["available", "created", "updated", "category"]
    list_editable = ["available"]
    prepopulated_fields = {"slug": ("name",)}

    inlines = [ProductFileInline, ProductImageInline]

    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE(
                attrs={"cols": 80, "rows": 30},
                mce_attrs=settings.TINYMCE_DEFAULT_CONFIG,
            )
        },
    }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        files = request.FILES.getlist("multiple_documents")
        for f in files:
            pass


from django.apps import apps
def get_contact_page_model():
    return apps.get_model('NFCLabs', 'ContactPage')

class ContactPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'show_contact_form', 'order', 'is_active']
    list_filter = ['is_active', 'show_contact_form']
    search_fields = ['name', 'content']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active', 'show_contact_form']
    
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('Settings', {
            'fields': ('show_contact_form', 'order', 'is_active')
        })
    )

try:
    ContactPage = get_contact_page_model()
    admin.site.register(ContactPage, ContactPageAdmin)
except Exception as e: 
    print(f"Error registering ContactPage: {e}")  
    pass