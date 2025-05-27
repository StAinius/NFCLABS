from NFCLabs.models import Category, Solution, ContactPage

def global_context(request):
    return {
        'categories': Category.objects.all(),
        'solutions': Solution.objects.all(),
        'contact_pages': ContactPage.objects.filter(is_active=True),
    }
    