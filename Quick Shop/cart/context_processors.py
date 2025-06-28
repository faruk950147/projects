from cart.models import Cart, Order

def carts_views(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, purchased=False)
        if carts.exists():
            return {'carts': carts}
        else:
            return {} 
    else:
        return {}

def carts_conuts(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False)
        if order.exists():
            carts_conuts = order[0].order_items.count()
            return {'carts_conuts': carts_conuts}
        else:
            return {} 
    else:
        return {}
    
def variation_total_price(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, purchased=False)
        if carts.exists():
            variation_total_price = carts[0].variation_total_price()
            return {'variation_total_price': variation_total_price}
        else:
            return {} 
    else:
        return {}   
    
def totals_price(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False)
        if order.exists():
            totals_price = order[0].totals_price()
            return {'totals_price': totals_price}
        else:
            return {} 
    else:
        return {}