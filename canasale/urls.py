from django.urls import path
from . import views

app_name = 'canasale'

urlpatterns = [
    # Canasale API Root
    path('', views.api_root, name='api_root'),
    
    # System Configuration
    path('config/', views.system_config, name='system_config'),
    
    # ERP Integration
    path('erp/', views.erp_integration, name='erp_integration'),
    
    # Admin Panels
    path('panels/', views.admin_panels, name='admin_panels'),
] 