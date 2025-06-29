from django.db import models
from django.urls import reverse
from tinymce.widgets import TinyMCE
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class Solution(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    details = models.TextField()
    image = models.ImageField(upload_to="solutions/", null=True, blank=True)

    video_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Video"
    )
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("solution_detail", args=[self.slug])

    class Meta:
        app_label = "NFCLabs"


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        app_label = "NFCLabs"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products_category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    class Meta:
        app_label = "NFCLabs"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    is_main = models.BooleanField(default=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.title or 'Image'}"

    class Meta:
        ordering = ["order"]
        app_label = "NFCLabs"

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(
                id=self.id
            ).update(is_main=False)
        elif not ProductImage.objects.filter(
            product=self.product, is_main=True
        ).exists():
            self.is_main = True
        super().save(*args, **kwargs)


class ProductFile(models.Model):
    product = models.ForeignKey(Product, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to="product_files/")
    title = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.file.name}"

    def clean(self):
        if not self.title:
            raise ValidationError({"title": "Title field is required."})
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        app_label = "NFCLabs"



class ContactPage(models.Model):
    name = models.TextField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='contact_pages/', blank=True, null=True)
    content = models.TextField(help_text="Puslapio turinys")
    show_contact_form = models.BooleanField(default=False, help_text="Ar rodyti kontaktinę formą šiame puslapyje?")
    order = models.IntegerField(default=0, help_text="Rikiavimo tvarka dropdown meniu")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    form_type = models.CharField(
    max_length=20, 
    choices=[
        ('contact', 'Contact Form'),
        ('partner', 'Partner Form'),
        ('quote', 'Quote Form')
    ], 
        default='contact'
    )
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Pages"
        app_label = 'NFCLabs'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('contact_detail', args=[self.slug])
    
class EmailConfig(models.Model):
    name = models.CharField(max_length=50, default="Email Configuration")
    email_host = models.CharField(
        max_length=200, 
        default="gandras.serveriai.lt",
        verbose_name="Email Host",
        help_text="SMTP server address"
    )
    email_port = models.IntegerField(
        default=465,
        verbose_name="Email Port",
        help_text="SMTP server port"
    )
    email_use_ssl = models.BooleanField(
        default=True,
        verbose_name="Use SSL",
        help_text="Enable SSL encryption"
    )
    email_use_tls = models.BooleanField(
        default=False,
        verbose_name="Use TLS",
        help_text="Enable TLS encryption"
    )
    email_host_user = models.EmailField(
        default="ainius@nfc.lt",
        verbose_name="Email Host User",
        help_text="SMTP username/email"
    )
    email_host_password = models.CharField(
        max_length=200,
        verbose_name="Email Host Password",
        help_text="SMTP server password"
    )
    default_from_email = models.CharField(
        max_length=200,
        default="Užklausa <ainius@nfc.lt>",
        verbose_name="Default From Email",
        help_text="Default sender email format"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Email Configuration"
        verbose_name_plural = "Email Configuration"
        
    def __str__(self):
        return f"Email Config ({self.email_host})"
    
    def save(self, *args, **kwargs):
        if not self.pk and EmailConfig.objects.exists():
            raise ValueError('Only one Email Configuration can exist')
        return super().save(*args, **kwargs)