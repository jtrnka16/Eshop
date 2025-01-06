from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import get_object_or_404

def store(request):
    all_products = Product.objects.all()

    context = {'my_products': all_products}

    return render(request, 'store/store.html', context=context)

def categories(request):
    all_categories = Category.objects.all()

    return {'all_categories':all_categories}

from django.core.paginator import Paginator

def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category).order_by('name')  # Default order

    # Handle Ajax requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        sort_by = request.GET.get('sort_by', 'name')
        if query:
            products = products.filter(name__icontains=query)
        products = products.order_by(sort_by)  # Apply sorting for Ajax requests

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
    paginator = Paginator(products, 10)  # Pagination after ordering
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/list-category.html', {
        'category': category,
        'products': page_obj
    })


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {'product': product}

    return render(request, 'store/product-info.html', context=context)

