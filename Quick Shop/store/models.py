from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from based.models import BasedModels

User = get_user_model()

# Create your models here.

class Category(BasedModels):
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    cat_image = models.ImageField(upload_to='category', null=True, blank=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True,blank=True)
    featured = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '1. Categories'
        

    @property
    def image_tag(self):   
        if self.cat_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.cat_image.url))
        else:
            self.cat_image

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

class Brand(BasedModels):
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    bra_image = models.ImageField(upload_to='brand', null=True, blank=True)
    featured = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '2. Brands'
        
    @property
    def image_tag(self):   
        if self.bra_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.bra_image.url))
        else:
            self.bra_image

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

class Product(BasedModels):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='bra_products')
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    price = models.PositiveIntegerField(default=0)
    old_price = models.PositiveIntegerField(default=0)
    in_stock_total = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    description = models.TextField(default='N/A')
    additiona_des = models.TextField(default='N/A')
    shipping_return = models.TextField(default='N/A')
    featured = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    top_deals = models.BooleanField(default=False)
    popular  = models.BooleanField(default=False)
    new_arrivals = models.BooleanField(default=False)
    recommendation = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '3. Products'
    
    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def discount_price(self):
        if self.discount:
            discount_price = self.price - ((self.discount / 100) * self.price)
            return discount_price
        else:
            return self.price

    def __str__(self):
        return f'{self.title}'
    
class ProductImages(BasedModels):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_images')
    gallery = models.ImageField(upload_to='product', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '4. Products Images'
        
    @property
    def image_tag(self):   
        if self.gallery:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.gallery.url))
        else:
            self.gallery
 
    def __str__(self):
        return f'{str(self.product.title)}'
    
class VariationManager(models.Manager):    
    def colors(self):
        return super(VariationManager, self).filter(variation='color')        
        
    def sizes(self):
        return super(VariationManager, self).filter(variation='size')

VARIATIONS_TYPES = (
    ('color', 'color'),
    ('size', 'size'),
    ('none', 'none'),
)
class Variations(BasedModels):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    variation = models.CharField(max_length=150, choices=VARIATIONS_TYPES, default='none')
    title = models.CharField(max_length=150, null=False, blank=False)
    variation_image = models.ImageField(upload_to='variaton', null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    objects = VariationManager()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '5. Variations'
        
    @property
    def image_tag(self):   
        if self.variation_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.variation_image.url))
        else:
            self.variation_image

    def __str__(self):
        return f'{self.title}'
   
class BannerOverlay(BasedModels):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='banner_overlay')
    title = models.CharField(max_length=150, unique=True, null=True, blank=True)
    off = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = '6. BannerOverlay'

    def __str__(self):
        return f'{self.title}'
    
class DealsOutlet(BasedModels):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='deals_outlet')
    title = models.CharField(max_length=150, unique=True, null=True, blank=True)
    pragh = models.CharField(max_length=150, null=True, blank=True)
    limit = models.PositiveIntegerField(default=1)
    deal_image = models.ImageField(upload_to='deals', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '7. Deals & Outlet'
        
    @property
    def deal_image(self):   
        if self.variaton_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.deal_image.url))
        else:
            self.deal_image

    def __str__(self):
        return f'{self.title}'