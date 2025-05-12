from django.contrib import admin
from .models import Category, Product, ProductFile, Solution, ProductImage

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

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
    list_display = ['name', 'category', 'available', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
    
    inlines = [ProductFileInline, ProductImageInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        files = request.FILES.getlist('multiple_documents')
        for f in files:
            pass

