import json
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.forms import modelformset_factory
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Category, Product, ProductFile, Solution, ContactPage
from .forms import ContactForm, PartnerForm, QuoteForm
from website_content.models import PageContent

logger = logging.getLogger(__name__)


def get_page_content(page_key):
    try:
        return PageContent.objects.get(page_key=page_key)
    except PageContent.DoesNotExist:
        return None


def home(request):
    page_content = get_page_content("home")
    return render(request, "pages/home.html", {"page_content": page_content})


def solutions(request):
    categories = Category.objects.all()
    solutions = Solution.objects.all()
    page_content = get_page_content("solutions")
    return render(
        request,
        "pages/solutions.html",
        {
            "categories": categories,
            "solutions": solutions,
            "page_content": page_content,
        },
    )


def solution_detail(request, slug):
    solution = get_object_or_404(Solution, slug=slug)

    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")

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

        return redirect("solution_detail", slug=slug)

    return render(request, "pages/solutions-detail.html", {"solution": solution})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")

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

        return redirect("product_detail", slug=slug)

    return render(request, "products/detail.html", {"product": product})


def about(request):
    categories = Category.objects.all()
    page_content = get_page_content("about")
    return render(
        request,
        "pages/about.html",
        {"categories": categories, "page_content": page_content},
    )


def contact(request):
    categories = Category.objects.all()
    page_content = get_page_content("contact")
    success_message = None
    contact_pages = ContactPage.objects.filter(is_active=True).order_by('order')

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                send_form_email(form.cleaned_data, 'contact')
                success_message = "Your message was sent successfully! We will contact you shortly."
                form = ContactForm()
            except Exception as e:
                pass
    else:
        form = ContactForm()

    return render(
        request,
        "pages/contact.html",
        {
            "categories": categories,
            "form": form,
            "page_content": page_content,
            "success_message": success_message,
            "contact_pages": contact_pages,
        },
    )


def products_list(request):
    categories = Category.objects.all()
    page_content = get_page_content("products")
    return render(
        request,
        "products/products_list.html",
        {"categories": categories, "page_content": page_content},
    )


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

    return render(
        request,
        "products/products_category.html",
        {"category": category, "products": products},
    )


def privacy_policy(request):
    page_content = get_page_content("privacy_policy")
    return render(request, "footer/privacy-policy.html", {"page_content": page_content})


def terms_of_service(request):
    page_content = get_page_content("terms_of_service")
    return render(
        request, "footer/terms-of-service.html", {"page_content": page_content}
    )


def cookie_policy(request):
    page_content = get_page_content("cookie_policy")
    return render(request, "footer/cookie-policy.html", {"page_content": page_content})


def contact_detail(request, slug):
    contact_page = get_object_or_404(ContactPage, slug=slug, is_active=True)

    form_classes = {"contact": ContactForm, "partner": PartnerForm, "quote": QuoteForm}

    FormClass = form_classes.get(contact_page.form_type, ContactForm)
    form = FormClass()

    related_pages = ContactPage.objects.filter(is_active=True).exclude(
        id=contact_page.id
    )

    if request.method == "POST" and contact_page.show_contact_form:
        form = FormClass(request.POST)
        if form.is_valid():
            try:
                send_form_email(form.cleaned_data, contact_page.form_type)
                messages.success(request, "Your message has been sent successfully!")
                return redirect("contact_detail", slug=slug)
            except Exception as e:
                messages.error(
                    request,
                    "There was an error sending your message. Please try again.",
                )

    context = {
        "contact_page": contact_page,
        "form": form if contact_page.show_contact_form else None,
        "pages": related_pages,
    }

    return render(request, "pages/contact_detail.html", context)


def send_form_email(cleaned_data, form_type):
    try:
        from .models import EmailConfig
        email_config = EmailConfig.objects.first()
        if email_config:
            from_email = email_config.default_from_email
            to_email = email_config.email_host_user
            
            from django.core.mail import get_connection
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=email_config.email_host,
                port=email_config.email_port,
                username=email_config.email_host_user,
                password=email_config.email_host_password,
                use_tls=email_config.email_use_tls,
                use_ssl=email_config.email_use_ssl,
            )
        else:
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = settings.EMAIL_HOST_USER
            connection = None
            
    except Exception as e:
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = settings.EMAIL_HOST_USER
        connection = None
    
    if form_type == "partner":
        subject = f"New Partnership Application: {cleaned_data['company_name']}"
        message = f"""
PARTNERSHIP APPLICATION

Company Information:
Company Name: {cleaned_data['company_name']}
Business Address: {cleaned_data['business_address']}
Country: {cleaned_data['country']}
Business Type: {cleaned_data.get('business_type', 'N/A')}
Website: {cleaned_data.get('website', 'N/A')}

Contact Person:
Name: {cleaned_data['contact_name']}
Position: {cleaned_data['position_title']}
Email: {cleaned_data['email']}
Phone: {cleaned_data['phone']}

Additional Message:
{cleaned_data.get('message', 'N/A')}
        """

    elif form_type == "quote":
        subject = f"New Quote Request: {cleaned_data['company']}"
        message = f"""
QUOTE REQUEST

Contact Information:
Name: {cleaned_data['name']}
Company: {cleaned_data['company']}
Email: {cleaned_data['email']}
Phone: {cleaned_data['phone']}

Request Details:
Products/Services: {cleaned_data['product_interest']}
Estimated Quantity: {cleaned_data.get('quantity', 'N/A')}
Budget Range: {cleaned_data.get('budget_range', 'N/A')}
Project Timeline: {cleaned_data.get('project_timeline', 'N/A')}
        """

    else:
        subject = f"New Contact Form Submission: {cleaned_data['subject']}"
        message = f"""
Name: {cleaned_data['name']}
Email: {cleaned_data['email']}
Company: {cleaned_data.get('company', 'N/A')}
Phone: {cleaned_data.get('phone', 'N/A')}

Message:
{cleaned_data['message']}
        """
    
    if connection:
        from django.core.mail import EmailMessage
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[to_email],
            connection=connection
        )
        result = email.send()
    else:
        result = send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False,
        )