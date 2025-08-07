from django.urls import path
from .views import raffle_draw

urlpatterns = [
    path('', raffle_draw, name='raffle_draw'),
]
