from django.urls import path
from . import views

app_name = 'weedvader'

urlpatterns = [
    # WeedVader API Root
    path('', views.api_root, name='api_root'),
    
    # Marketplace
    path('marketplace/', views.marketplace, name='marketplace'),
    
    # Marketplace Listings
    path('listings/', views.marketplace_listings, name='marketplace_listings'),
    
    # Marketplace Orders
    path('orders/', views.marketplace_orders, name='marketplace_orders'),
    
    # Card Payments
    path('payments/', views.card_payments, name='card_payments'),
] 