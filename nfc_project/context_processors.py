def categories_processor(request):
    """
    Context processor to make categories available in all templates.
    """
    from .models import Category, Solution
    
    categories = Category.objects.all()
    
    return {
        'categories': categories,
    }

def solutions_processor(request):
    from .models import Solution
    return {'solutions': Solution.objects.all()}

    
def categories_processor(request):
    from .models import Category, Solution
    
    categories = Category.objects.all()
    
    return {
        'categories': categories,
    }

def solutions_processor(request):
    from .models import Solution
    return {'solutions': Solution.objects.all()}
