from django.urls import path
from . import views

app_name = 'wallets'

urlpatterns = [
    # Wallets API Root
    path('', views.api_root, name='api_root'),
    
    # Wallet Types
    path('types/', views.wallet_types_list, name='wallet_types_list'),
    
    # Wallets
    path('list/', views.wallets_list, name='wallets_list'),
    
    # Wallet Addresses  
    path('addresses/', views.wallet_addresses_list, name='wallet_addresses_list'),
    
    # Wallet Transactions
    path('transactions/', views.wallet_transactions_list, name='wallet_transactions_list'),
] 