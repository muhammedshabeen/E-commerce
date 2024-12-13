from backend.models import Cart

def cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()
    return {'cart_count': cart_count}