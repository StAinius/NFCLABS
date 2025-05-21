from django.contrib import admin
from django.db import models
from .models import Category, Product, ProductFile, Solution, ProductImage
from tinymce.widgets import TinyMCE
from django.conf import settings


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
