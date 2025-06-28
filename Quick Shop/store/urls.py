from django.urls import path
from store.views import (
    HomeView, ProductView, ProductListView, Filter_Data, Load_More_Data
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product_list', ProductListView.as_view(), name='product_list'),
    path('product_details/<str:slug>/<uuid:id>/', ProductView.as_view(), name='product_details'),
    path('filter_data/',Filter_Data, name="filter_data"),
    path('load_more_data/',Load_More_Data, name="load_more_data"),
]
