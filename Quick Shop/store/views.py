from django.shortcuts import render,redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Min, Max

#import store models
from store.models import (
    Category, Brand, Product, ProductImages, Variations
)
# Create your views here.

@method_decorator(never_cache, name='dispatch')
class HomeView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    def get(self, request):
        popular_categories = Category.objects.filter(status=True, popular=True).order_by('-id')
        featured_categories = Category.objects.filter(status=True, featured=True).order_by('-id')
        new_arrivals = Product.objects.filter(status=True, in_stock=True, new_arrivals=True).order_by('-id')[:6] 
        trending = Product.objects.filter(status=True, in_stock=True, trending=True).order_by('-id')[:6] 
        recommendation = Product.objects.filter(status=True, in_stock=True, recommendation=True).order_by('-id')[:6] 
        context = {
            'popular_categories': popular_categories,
            'featured_categories': featured_categories,
            'new_arrivals': new_arrivals,
            'trending': trending,
            'recommendation': recommendation,
        }
        return render(request, 'store/home.html', context)
       
@method_decorator(never_cache, name='dispatch')    
class ProductView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    def get(self, request, slug, id):
        product = get_object_or_404(Product, slug=slug, id=id)
        related_products = Product.objects.filter(category=product.category).exclude(id=id).order_by('-id')[:4]
        context = {
            'product': product,
            'related_products': related_products,
        }
        return render(request, 'store/product.html', context)
    
@method_decorator(never_cache, name='dispatch')    
class ProductListView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    def get(self, request):
        products = Product.objects.filter(status=True, in_stock=True).all().order_by('-id')[:3]
        paginate_by = 3
        context = {
            'products': products,
            'paginate_by': paginate_by,
        }
        return render(request, 'store/product_list.html', context)
    
def Filter_Data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    minPrice=request.GET.get('minPrice')
    maxPrice=request.GET.get('maxPrice')
    products = Product.objects.all().order_by('-id')
    
    if len(minPrice):
        products=products.filter(price__gte=minPrice)
        
    if len(maxPrice):
        products=products.filter(price__lte=maxPrice)
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
    
    if len(brands) > 0:
        products = products.filter(brand__id__in=brands).distinct()

    t = render_to_string('ajax/ajax.html', {'products': products})

    return JsonResponse({'products': t})

def Load_More_Data(request):
	offset = int(request.GET.get('offset'))
	limit = int(request.GET.get('limit'))
	products = Product.objects.all().order_by('-id')[offset:offset+limit]
	t = render_to_string('ajax/ajax.html',{'products':products})
	return JsonResponse({'products': t})