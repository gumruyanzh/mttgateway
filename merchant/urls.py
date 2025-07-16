from django.urls import path
from . import views

app_name = 'merchant'

urlpatterns = [
    # Merchant API Root
    path('', views.api_root, name='api_root'),
    
    # Merchants
    path('list/', views.merchants_list, name='merchants_list'),
    
    # Merchant Gateways
    path('gateways/', views.merchant_gateways_list, name='merchant_gateways_list'),
    
    # Merchant Products
    path('products/', views.merchant_products_list, name='merchant_products_list'),
    
    # Merchant Transactions
    path('transactions/', views.merchant_transactions_list, name='merchant_transactions_list'),
] 