from cart.models import Cart, CartItem
from cart.views import _get_cart_id


def counter(request):
    cart_items_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_items_count += cart_item.quantity
        except Cart.DoesNotExist:  # ToDo: Is this try/except block necessary? Cart.objects.filter vs get...
            cart_items_count = 0

    return {'cart_items_count': cart_items_count}