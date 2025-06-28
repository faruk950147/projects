from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from based.models import BasedModels
from store.models import Product, Variations
User = get_user_model()

# Create your models here.

class Cart(BasedModels):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    color_variant = models.CharField(max_length=250, blank=True, null=True)
    size_variant = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    total = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '1. Carts'
        

    def total_price(self):
        return self.quantity * self.item.price
        
    def variation_total_price(self):
        colors = Variations.objects.filter(variation='color', product=self.item)
        sizes = Variations.objects.filter(variation='size', product=self.item)
        color_price = 0
        size_price = 0
        if colors.exists() and sizes.exists():
            for color in colors:
                if color.title == self.color_variant:
                    color_price = color.price * self.quantity       
            for size in sizes:
                if size.title == self.size_variant:
                    size_price = size.price * self.quantity
            color_price_size_price = color_price + size_price
            return color_price_size_price
                
        if colors.exists():
            for color in colors:
                if color.title == self.color_variant:
                    color_price = color.price * self.quantity
                    return color_price
                
        if sizes.exists():
            for size in sizes:
                if size.title == self.size_variant:
                    size_price = size.price * self.quantity
                    return size_price
                
        return False
    
    def __str__(self):
        return f'{self.quantity} X {self.item} X {self.purchased}'
    
class Order(BasedModels):
    PAYMENT_METHOD = (
         ('Cash on Delivery', 'Cash on Delivery'),
         ('Paypal', 'Paypal'),
         ('SSLcommerz', 'SSLcommerz'),
     )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    order_id = models.CharField(max_length=250, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='Cash on Delivery')
    totals = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '2. Orders'
        

    def total_items(self):
        total_items = self.order_items.count()
        return total_items
    
    
    def totals_price(self):
        total = 0
        for order_item in self.order_items.all():
            if order_item.variation_total_price():
                total += order_item.variation_total_price()
            else:
                total += order_item.total_price()
        return total

    def __str__(self):
        return f'{self.user} X {self.order_items} X {self.ordered}'