from django.db.models import Sum

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart_item_count = request.user.cart.cartitems.filter(is_order_placed=False).count()
        if cart_item_count > 0:
            data = request.user.cart.cartitems.filter(is_order_placed=False).aggregate(total=Sum('quantity'))
            count = data.get('total')
    return {'item_count': count}

