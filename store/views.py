from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import get_object_or_404

def store(request):
    query = request.GET.get('q')
    all_products = Product.objects.all()
    main_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    # Vyhledávání produktů
    if query:
        all_products = all_products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'my_products': all_products,
        'main_categories': main_categories,
        'query': query  # Přidáme dotaz do kontextu pro případné zobrazení na stránce
    }

    return render(request, 'store/store.html', context)

def categories(request):
    main_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

    return {'main_categories': main_categories}

def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    subcategories = category.subcategories.all()
    all_categories = [category] + list(subcategories)

    products = Product.objects.filter(category__in=all_categories).order_by('name')

    # Handle Ajax requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        sort_by = request.GET.get('sort_by', 'name')
        if query:
            products = products.filter(name__icontains=query)
        products = products.order_by(sort_by)

        paginator = Paginator(products, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        products_data = [
            {
                'name': product.name,
                'price': product.price,
                'slug': product.slug,
                'image': request.build_absolute_uri(product.image.url) if product.image else None
            }
            for product in page_obj
        ]

        return JsonResponse({
            'products': products_data,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        })

    # Pagination for initial render
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/list-category.html', {
        'category': category,
        'products': page_obj,
        'subcategories': subcategories,  # Přidá subkategorie pro zobrazení v šabloně
    })

def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {'product': product}

    return render(request, 'store/product-info.html', context=context)

