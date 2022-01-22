from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem
from store.models import Product, Variation


def _get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_variations = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variations.append(variation)
            except Variation.DoesNotExist:
                pass

    try:
        user_cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        user_cart = Cart.objects.create(cart_id=_get_cart_id(request))

    cart_item_exists = CartItem.objects.filter(product=product, cart=user_cart).exists()
    if cart_item_exists:  # ToDo: Use := operator and instead of checking that cart_item exists, use filter() and fetch the queryset directly
        cart_item = CartItem.objects.filter(product=product, cart=user_cart)
        existing_variation_list = []
        id = []  # ToDo: Rename the variable as this one shadows the built-in one.
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))  # ToDo: Convert queryset to list while getting the existing_variation
            id.append(item.id)  # ToDo: Use values_list() to get ids from cart_item queryset.

        if product_variations in existing_variation_list:
            index = existing_variation_list.index(product_variations)  # ToDo: Use enumarate() instead of this.
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=user_cart)
            if len(product_variations) > 0:  # ToDo: This is ugly, use 'if product_variations'.
                item.variations.clear()
                item.variations.add(*product_variations)
            item.save()  # ToDo: Remove save() as create() and clear() apply db changes immediately.
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=user_cart)
        if len(product_variations) > 0:  # ToDo: This is ugly, use 'if product_variations'.
            cart_item.variations.clear()
            cart_item.variations.add(*product_variations)
        cart_item.save()  # ToDo: Remove save() as create(), clear() and add() apply db changes immediately.

    return redirect('cart')


def remove_from_cart(request, product_id, cart_item_id):
    user_cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, pk=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=user_cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:  # ToDo: Specify the exception.
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    user_cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, pk=product_id)
    cart_item = CartItem.objects.get(product=product, cart=user_cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


def cart(request, total_price=0, quantity=0, cart_items=None):
    try:
        user_cart = Cart.objects.get(cart_id=_get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=user_cart, is_active=True)
        for item in cart_items:
            total_price += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (total_price * 0.21)
        total_price_vat = total_price + tax
    except Cart.DoesNotExist:
        pass

    context = {'total_price': total_price, 'quantity': quantity, 'cart_items': cart_items, 'tax': tax, 'total_price_vat': total_price_vat}  # ToDo: fix this referencing befor assignment (app fails when accesing a cart section directly before adding any item to cart)

    return render(request, 'store/cart.html', context)
