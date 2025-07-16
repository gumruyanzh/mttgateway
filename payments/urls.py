from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payments API Root
    path('', views.api_root, name='api_root'),
    
    # Payment Methods
    path('methods/', views.payment_methods_list, name='payment_methods_list'),
    
    # Payment Transactions
    path('transactions/', views.payment_transactions_list, name='payment_transactions_list'),
    
    # Exchange Rates
    path('rates/', views.exchange_rates_list, name='exchange_rates_list'),
] 