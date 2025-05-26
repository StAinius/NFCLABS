from NFCLabs.models import Category, Solution, ContactPage

def categories_processor(request):
    from .models import Category

    categories = Category.objects.all()

    return {
        "categories": categories,
    }


def solutions_processor(request):
    from .models import Solution

    return {"solutions": Solution.objects.all()}


def contact_pages_processor(request):
    return {
        'contact_pages': ContactPage.objects.filter(is_active=True),
    }