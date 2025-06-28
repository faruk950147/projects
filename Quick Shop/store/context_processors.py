from django.shortcuts import redirect
from django.db.models import Min, Max
from store.models import (
    Category, Brand, Product, ProductImages, Variations
)

def get_filters(request):
    categories = Category.objects.filter(status=True, parent=None).all().order_by('-id')
    cats = Category.objects.filter(status=True).all().order_by('-id')
    brands = Brand.objects.filter(status=True).all().order_by('-id')
    total_data = Product.objects.count()
    minPrice = Product.objects.all().aggregate(Min('price'))
    maxPrice = Product.objects.all().aggregate(Max('price'))
    return {
        'categories': categories,
        'cats': cats,
        'brands': brands,
        'total_data': total_data,
        'minPrice': minPrice,
        'maxPrice': maxPrice,
    }

def discount_price(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        if products.exists():
            discount_price = products[0].discount_price()
            return {'discount_price': discount_price}
        else:
            return {} 
    else:
        return {} 