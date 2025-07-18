"""
URL configuration for mtt_gateway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Homepage
    path('', views.homepage, name='homepage'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Module APIs
    path('api/merchant/', include('merchant.urls')),
    path('api/canasale/', include('canasale.urls')),
    path('api/maythetoken/', include('maythetoken.urls')),
    path('api/weedvader/', include('weedvader.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/wallets/', include('wallets.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/tokens/', include('tokens.urls')),
    
    # Authentication
    path('api/auth/', include('rest_framework.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site headers
admin.site.site_header = "MTT Gateway Administration"
admin.site.site_title = "MTT Gateway Admin"
admin.site.index_title = "Welcome to MTT Gateway Administration"
