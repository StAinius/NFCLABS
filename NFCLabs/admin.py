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
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image')
        }),
        ('Content', {
            'fields': ('description', 'details'),
            'classes': ('wide',)
        }),
        ('Video', {
            'fields': ('video_url',),
            'description': 'Video URL'
        }),
    )

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
    return apps.get_model("NFCLabs", "ContactPage")


class ContactPageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "form_type",
        "show_contact_form",
        "order",
        "is_active",
    ]
    list_filter = ["is_active", "show_contact_form", "form_type"]
    search_fields = ["name", "content"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order", "is_active", "show_contact_form", "form_type"]

    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }

    fieldsets = (
        (None, {"fields": ("name", "slug", "image")}),
        ("Content", {"fields": ("content",), "classes": ("wide",)}),
        ("Form Settings", {"fields": ("form_type", "show_contact_form")}),
        ("Settings", {"fields": ("order", "is_active")}),
    )


try:
    ContactPage = get_contact_page_model()
    admin.site.register(ContactPage, ContactPageAdmin)
except Exception as e:
    print(f"Error registering ContactPage: {e}")
    pass

from .models import EmailConfig
class EmailConfigForm(forms.ModelForm):
    email_host_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password...'}),
        label="Email Host Password",
        help_text="SMTP server password"
    )
    
    class Meta:
        model = EmailConfig
        fields = '__all__'

@admin.register(EmailConfig)
class EmailConfigAdmin(admin.ModelAdmin):
    form = EmailConfigForm
    list_display = ['name', 'email_host', 'email_host_user', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        return not EmailConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        ('Basic Settings', {
            'fields': ('name',)
        }),
        ('SMTP Server Settings', {
            'fields': ('email_host', 'email_port', 'email_use_ssl', 'email_use_tls')
        }),
        ('Authentication', {
            'fields': ('email_host_user', 'email_host_password')
        }),
        ('Email Format', {
            'fields': ('default_from_email',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )