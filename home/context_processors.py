from order.models import ShopCart


def shopcart(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    
    return {
        "shopcart_counter" : shopcart.count,
    }
