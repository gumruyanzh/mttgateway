from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def api_root(request):
    """
    Canasale API Root - Available endpoints
    """
    return Response({
        'message': 'MTT Gateway - Canasale API',
        'version': '1.0',
        'endpoints': {
            'system_config': '/api/canasale/config/',
            'erp_integration': '/api/canasale/erp/',
            'admin_panels': '/api/canasale/panels/',
        },
        'description': 'ERP integration, admin panels, and system configuration',
        'status': 'Active'
    })

@api_view(['GET'])
def system_config(request):
    """
    System configuration endpoint
    """
    return Response({
        'message': 'System configuration endpoint',
        'status': 'Available',
        'note': 'Configuration management is active'
    })

@api_view(['GET'])
def erp_integration(request):
    """
    ERP integration endpoint
    """
    return Response({
        'message': 'ERP integration endpoint',
        'status': 'Available',
        'note': 'ERP integration services are ready'
    })

@api_view(['GET'])
def admin_panels(request):
    """
    Admin panels endpoint
    """
    return Response({
        'message': 'Admin panels endpoint',
        'status': 'Available',
        'note': 'Admin panel management is active'
    })
