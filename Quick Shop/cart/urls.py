from django.urls import path
from cart.views import (
    AddToCart
)

urlpatterns = [
    path('add_to_cart/<str:slug>/<uuid:id>/', AddToCart.as_view(), name='add_to_cart'),
]
