from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from cart.models import CartItem
from cart.views import _get_cart_id
from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    categories = None  # ToDo: This have no usage here...?
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('-id')
        paginator = Paginator(products, 1)  # ToDo: Remove redundant paginator related code
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    context = {'products': paged_products}
    return render(request, 'store/store.html', context=context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product=single_product)
    except Product.DoesNotExist:
        return HttpResponse("Not found")

    context = {'single_product': single_product, 'in_cart': in_cart}

    return render(request, 'store/product_detail.html', context=context)


def search(request):
    if 'keyword' in request.GET:  # ToDo: This is not a nice code....use := operator and dict.get() method instead
        keyword = request.GET['keyword']
        if keyword:  # ToDo: Add else condition to filter all products case of empty string search (now it raises an error)
            products = Product.objects.filter(Q(slug__icontains=keyword) | Q(product_name=keyword), is_available=True, ).order_by('-id')

    context = {'products': products}
    return render(request, 'store/store.html', context=context)

