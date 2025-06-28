from django.shortcuts import render,redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse

from store.models import Product
from cart.models import Cart, Order
# Create your views here.

@method_decorator(never_cache, name='dispatch')
class AddToCart(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    def post(self, request, slug, id):
        if request.user.is_authenticated:
            #get product id slug from requested url
            item = get_object_or_404(Product, slug=slug, id=id)
            #get product select_color select_size quantity from requested frontend
            select_color = request.POST.get('select_color')
            select_size = request.POST.get('select_size')
            quantity = request.POST.get('quantity')
            #get & check product is already exists or not in cart database
            cart_item = Cart.objects.get_or_create(
            item=item, user=request.user, purchased=False
            )
            #get order object
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            if order_qs.exists():
                #tuple convert to indexing object
                order = order_qs[0]                
                if order.order_items.filter(item=item).exists():
                    if quantity:
                        cart_item[0].quantity += int(quantity)
                    else:
                        cart_item[0].quantity += 1
                    cart_item[0].color_variant = select_color
                    cart_item[0].size_variant = select_size
                    cart_item[0].save()
                    messages.success(request, 'Your quantity updated')
                    return redirect('product_details', item.slug, item.id)
                else:
                    cart_item[0].color_variant = select_color
                    cart_item[0].size_variant = select_size
                    cart_item[0].save()
                    order.order_items.add(cart_item[0])
                    messages.success(request, 'Product added to your variation')
                    return redirect('product_details', item.slug, item.id)
            else:
                order = Order(user=request.user)
                order.save()
                order.order_items.add(cart_item[0])
                messages.success(request, 'Product added to your cart')
                return redirect('product_details', item.slug, item.id)
        else:
            return redirect('login')