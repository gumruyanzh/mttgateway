from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # Customers API Root
    path('', views.api_root, name='api_root'),
    
    # Customer Profiles
    path('profiles/', views.customer_profiles_list, name='customer_profiles_list'),
    
    # Customer KYC
    path('kyc/', views.customer_kyc_list, name='customer_kyc_list'),
    
    # Customer Activities
    path('activities/', views.customer_activities_list, name='customer_activities_list'),
] 