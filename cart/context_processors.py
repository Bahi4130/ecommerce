from cart.models import Cart, CartItem
from cart.views import _get_cart_id


def counter(request):
    cart_items_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_get_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart_items = CartItem.objects.filter(cart=cart[:1])  # ToDo: Would not be better to use last() instead of slicing?
            for cart_item in cart_items:
                cart_items_count += cart_item.quantity
        except Cart.DoesNotExist:  # ToDo: Is this try/except block necessary? Can filter() throw DoesNotExist exception?
            cart_items_count = 0

    return {'cart_items_count': cart_items_count}