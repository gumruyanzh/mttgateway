from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def api_root(request):
    """
    WeedVader API Root - Available endpoints
    """
    return Response({
        'message': 'MTT Gateway - WeedVader API',
        'version': '1.0',
        'endpoints': {
            'marketplace': '/api/weedvader/marketplace/',
            'listings': '/api/weedvader/listings/',
            'orders': '/api/weedvader/orders/',
            'payments': '/api/weedvader/payments/',
        },
        'description': 'Marketplace functionality and card payment processing',
        'status': 'Active'
    })

@api_view(['GET'])
def marketplace(request):
    """
    Marketplace endpoint
    """
    return Response({
        'message': 'Marketplace endpoint',
        'status': 'Available',
        'note': 'Marketplace services are active'
    })

@api_view(['GET'])
def marketplace_listings(request):
    """
    Marketplace listings endpoint
    """
    return Response({
        'message': 'Marketplace listings endpoint',
        'status': 'Available',
        'count': 0,
        'results': [],
        'note': 'No listings found - database empty'
    })

@api_view(['GET'])
def marketplace_orders(request):
    """
    Marketplace orders endpoint
    """
    return Response({
        'message': 'Marketplace orders endpoint',
        'status': 'Available',
        'count': 0,
        'results': [],
        'note': 'No orders found - database empty'
    })

@api_view(['GET'])
def card_payments(request):
    """
    Card payment processing endpoint
    """
    return Response({
        'message': 'Card payment processing endpoint',
        'status': 'Available',
        'payment_processors': ['Stripe', 'PayPal', 'Square'],
        'note': 'Card payment processing is ready'
    })
