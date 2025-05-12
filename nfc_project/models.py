from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django import forms
from django.core.exceptions import ValidationError

class Solution(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='solutions/', blank=True)
    details = RichTextField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('solution_detail', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = RichTextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.title or 'Image'}"
    
    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(id=self.id).update(is_main=False)
        elif not ProductImage.objects.filter(product=self.product, is_main=True).exists():
            self.is_main = True
        super().save(*args, **kwargs)

class ProductFile(models.Model):
    product = models.ForeignKey(Product, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='product_files/')
    title = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) 

    def __str__(self):
        return f"{self.product.name} - {self.file.name}"
    
    def clean(self):
        """Validate that the title is not empty"""
        if not self.title:
            raise ValidationError({'title': 'Title field is required.'})
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

