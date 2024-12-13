from django import template
from backend.models import Cart

register = template.Library()

@register.simple_tag
def cart_single_object(cart):
    print("ENETRED")
    total_amount = cart.product.price * cart.quantity
    return total_amount

@register.simple_tag
def cart_total(user):
    cart_objs = Cart.objects.filter(user=user)
    total_amount = sum(item.product.price * item.quantity for item in cart_objs)
    return total_amount

@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def to(value):
    return range(1, value + 1)