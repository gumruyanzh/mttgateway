from django.urls import path
from . import views

app_name = 'tokens'

urlpatterns = [
    # Tokens API Root
    path('', views.api_root, name='api_root'),
    
    # Tokens
    path('list/', views.tokens_list, name='tokens_list'),
    
    # Token Balances
    path('balances/', views.token_balances_list, name='token_balances_list'),
    
    # Token Transfers
    path('transfers/', views.token_transfers_list, name='token_transfers_list'),
    
    # Token Prices
    path('prices/', views.token_prices_list, name='token_prices_list'),
] 