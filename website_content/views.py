from website_content.models import PageContent
from django.shortcuts import render

def get_page_content(page_key):
    try:
        return PageContent.objects.get(page_key=page_key)
    except PageContent.DoesNotExist:
        return None

def get_meta_data(page_key):
    try:
        page_content = PageContent.objects.get(page_key=page_key)
        return {
            'meta_description': page_content.meta_description,
            'meta_keywords': page_content.meta_keywords,
        }
    except PageContent.DoesNotExist:
        return {
            'meta_description': "",
            'meta_keywords': "",
        }

