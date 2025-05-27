from django import forms
from .models import Product, ProductFile
from django.forms import modelformset_factory
from tinymce.widgets import TinyMCE


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    company = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Company"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your Email"}
        )
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Phone"}
        ),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Your Message", "rows": 5}
        )
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "slug", "available"]

    description = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))


class ProductFileForm(forms.ModelForm):
    class Meta:
        model = ProductFile
        fields = ["file"]


ProductFileFormSet = modelformset_factory(
    ProductFile, form=ProductFileForm, extra=5, can_delete=True
)


class PartnerForm(forms.Form):
    company_name = forms.CharField(
        max_length=200,
        label="Company Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    business_address = forms.CharField(
        label="Business Address",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Full business address including street, city, postal code",
            }
        ),
    )
    country = forms.CharField(
        max_length=100,
        label="Country",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    website = forms.CharField(
        required=False,
        label="Website",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "https://your-website.com"}
        ),
    )

    contact_name = forms.CharField(
        max_length=100,
        label="Contact Person Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    position_title = forms.CharField(
        max_length=100,
        label="Position / Title",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email Address", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        max_length=20,
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    message = forms.CharField(
        required=False,
        label="Additional Message",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell us more about your business or partnership interests...",
            }
        ),
    )


class QuoteForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    company = forms.CharField(
        max_length=100,
        label="Company",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        max_length=20,
        label="Phone",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    product_interest = forms.CharField(
        label="Products/Services of Interest",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Please describe the products or services you are interested in...",
            }
        ),
        help_text="Tell us what specific products or services you need",
    )
