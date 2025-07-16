from django.urls import path
from . import views

app_name = 'maythetoken'

urlpatterns = [
    # MayTheToken API Root
    path('', views.api_root, name='api_root'),
    
    # Trading Pairs
    path('pairs/', views.trading_pairs, name='trading_pairs'),
    
    # Trade Orders
    path('orders/', views.trade_orders, name='trade_orders'),
    
    # Liquidity Pools
    path('liquidity/', views.liquidity_pools, name='liquidity_pools'),
    
    # Routing Engine
    path('routing/', views.routing_engine, name='routing_engine'),
] 