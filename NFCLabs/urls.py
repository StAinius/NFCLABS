from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("solutions/", views.solutions, name="solutions"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('contact/<slug:slug>/', views.contact_detail, name='contact_detail'),
    path("products/", views.products_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("solutions/<slug:slug>/", views.solution_detail, name="solution_detail"),
    path(
        "products/category/<slug:slug>/",
        views.products_category,
        name="products_category",
    ),
    path("footer/privacy-policy/", views.privacy_policy, name="privacy-policy"),
    path("footer/terms-of-service/", views.terms_of_service, name="terms-of-service"),
    path("footer/cookie-policy/", views.cookie_policy, name="cookie-policy"),
    path("tinymce/", include("tinymce.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

