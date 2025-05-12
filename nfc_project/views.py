from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.forms import modelformset_factory
from django import forms

import json
import logging

from .models import Category, Product, ProductFile, Solution
from .forms import ContactForm

logger = logging.getLogger(__name__)



def home(request):
    return render(request, 'pages/home.html')

def solutions(request):
    categories = Category.objects.all()
    solutions = Solution.objects.all()
    return render(request, 'pages/solutions.html', {
        'categories': categories,
        'solutions': solutions
    })

def solution_detail(request, slug):
    solution = get_object_or_404(Solution, slug=slug)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        email_message = (
            f"Solution Interest: {solution.name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        )
        
        send_mail(
            subject=f"Interest in {solution.name} Solution",
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        
        return redirect('solution_detail', slug=slug)
    
    return render(request, 'pages/solutions-detail.html', {'solution': solution})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        email_message = (
            f"Product interest: {product.name}\n"
            f"Email: {email}\n\n"
            f"Message:\n{message}"
        )
        
        send_mail(
            subject=f"Interest in {product.name}",
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return redirect('product_detail', slug=slug)
    
    return render(request, 'products/detail.html', {'product': product})


def about(request):
    categories = Category.objects.all()
    return render(request, 'pages/about.html', {
        'categories': categories
    })

def contact(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            company = form.cleaned_data.get('company', '') 
            phone = form.cleaned_data.get('phone', '')  

            email_message = (
                f"Name: {name}\n"
                f"Company: {company}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n\n"
                f"Message:\n{message}"
            )

            
            send_mail(
                subject=f"Contact Form: {subject}",
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
                
            )
            
            messages.success(request, "Jūsų žinutė sėkmingai išsiųsta! Susisieksime artimiausiu metu.")
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'pages/contact.html', {
        'categories': categories,
        'form': form
    })

def products_list(request):
    categories = Category.objects.all()
    return render(request, 'products/products_list.html', {'categories': categories})

def products_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    for product in products:
        main_images = product.images.filter(is_main=True)
        if main_images.exists():
            product.main_image = main_images.first()
        elif product.images.exists():
            product.main_image = product.images.first()
        else:
            product.main_image = None
    
    return render(request, 'products/products_category.html', {
        'category': category,
        'products': products
    })
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    category = product.category
    
    class ProductFileForm(forms.ModelForm):
        class Meta:
            model = ProductFile
            fields = ('file', 'title')
        
        def clean_title(self):
            title = self.cleaned_data.get('title')
            if not title:
                raise forms.ValidationError("Title is required.")
            return title
    
    ProductFileFormSet = modelformset_factory(
        ProductFile, 
        form=ProductFileForm,
        extra=1
    )
    
    if request.method == 'POST':
        formset = ProductFileFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
        else:
            pass
    else:
        formset = ProductFileFormSet(queryset=ProductFile.objects.filter(product=product))
    
    return render(request, 'products/detail.html', {
        'product': product,
        'category': category,
        'formset': formset,
    })
    
def privacy_policy(request):
    return render(request, 'footer/privacy-policy.html')

def terms_of_service(request):
    return render(request, 'footer/terms-of-service.html')

def cookie_policy(request):
    return render(request, 'footer/cookie-policy.html')