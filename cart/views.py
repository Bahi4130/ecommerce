from django.shortcuts import render, redirect, get_object_or_404

from cart.models import Cart, CartItem
from store.models import Product


def _get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    try:
        user_cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        user_cart = Cart.objects.create(cart_id=_get_cart_id(request))

    try:
        cart_item = CartItem.objects.get(product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(product=product, quantity=1, cart=user_cart)

    return redirect('cart')


def remove_from_cart(request, product_id):
    user_cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, pk=product_id)
    cart_item = CartItem.objects.get(product=product, cart=user_cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    user_cart = Cart.objects.get(cart_id=_get_cart_id(request))
    product = get_object_or_404(Product, pk=product_id)
    cart_item = CartItem.objects.get(product=product, cart=user_cart)
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

    context = {'total_price': total_price, 'quantity': quantity, 'cart_items': cart_items, 'tax': tax, 'total_price_vat': total_price_vat}

    return render(request, 'store/cart.html', context)
