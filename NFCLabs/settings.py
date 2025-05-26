from pathlib import Path
from decouple import config
import os


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = "RENDER" not in os.environ

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")

SECRET_KEY = "django-insecure-#jtq0thhz2k8z^(jwth*f4aafddr^tq5zgyzbf1j2r)zr(galw"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True

DEBUG = True

ALLOWED_HOSTS = ['nfclabs.com', 'www.nfclabs.com', '89.40.6.100', 'localhost', '127.0.0.1']

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "website_content",
    "NFCLabs",
    "tinymce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "NFCLabs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "NFCLabs.context_processors.categories_processor",
                "NFCLabs.context_processors.solutions_processor",
                "NFCLabs.context_processors.contact_pages_processor",
            ],
        },
    },
]


WSGI_APPLICATION = "NFCLabs.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "static"]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "gandras.serveriai.lt"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = "ainius@nfc.lt"
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "Užklausa <ainius@nfc.lt>"

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

TINYMCE_JS_URL = "https://cdn.jsdelivr.net/npm/tinymce@5/tinymce.min.js"
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "plugins": "advlist autolink lists link searchreplace visualblocks code fullscreen insertdatetime media table wordcount textcolor",
    "toolbar1": "bold italic underline strikethrough | forecolor backcolor | removeformat | code",
    "toolbar2": "fontselect fontsizeselect | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link",
    "menubar": False,
    "statusbar": False,
    "font_formats": "Andale Mono=andale mono,times;"
    + "Arial=arial,helvetica,sans-serif;"
    + "Arial Black=arial black,avant garde;"
    + "Book Antiqua=book antiqua,palatino;"
    + "Comic Sans MS=comic sans ms,sans-serif;"
    + "Courier New=courier new,courier;"
    + "Georgia=georgia,palatino;"
    + "Helvetica=helvetica;"
    + "Impact=impact,chicago;"
    + "Roboto=roboto,sans-serif;"
    + "Symbol=symbol;"
    + "Tahoma=tahoma,arial,helvetica,sans-serif;"
    + "Terminal=terminal,monaco;"
    + "Times New Roman=times new roman,times;"
    + "Trebuchet MS=trebuchet ms,geneva;"
    + "Verdana=verdana,geneva;"
    + "Webdings=webdings;"
    + "Wingdings=wingdings,zapf dingbats;",
    "fontsize_formats": "8pt 9pt 10pt 11pt 12pt 14pt 16pt 18pt 20pt 22pt 24pt 28pt 36pt 48pt 72pt",
    "height": 300,
    "branding": False,
    "resize": "both",
    "elementpath": False,
}

JAZZMIN_SETTINGS = {
    "site_title": "NFC Labs",
    "site_header": "NFC Labs",
    "site_brand": "NFC Labs",
    "site_logo": "img/favicon.ico",
    "login_logo": "img/logo.png",
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "copyright": "UAB „Daglus“",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"app": "app"},
        {"name": "Site", "url": "/", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "mailto:support@nfclabs.lt", "new_window": True},
        {"name": "Docs", "url": "/docs/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "related_modal_active": True,
    "use_google_fonts_cdn": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app.Model": "fas fa-cube",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-teal",
    "navbar": "navbar-teal navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "sandstone",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
    "actions_sticky_top": False,
}
