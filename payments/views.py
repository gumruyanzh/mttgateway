from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def api_root(request):
    """
    Payments API Root - Available endpoints
    """
    return Response({
        'message': 'MTT Gateway - Payments API',
        'version': '1.0',
        'endpoints': {
            'methods': '/api/payments/methods/',
            'transactions': '/api/payments/transactions/',
            'exchange_rates': '/api/payments/rates/',
        },
        'description': 'Fiat-to-MTT conversion and payment processing system',
        'status': 'Active'
    })

@api_view(['GET'])
def payment_methods_list(request):
    """
    List payment methods
    """
    return Response({
        'message': 'Payment methods endpoint',
        'count': 0,
        'results': [],
        'note': 'No payment methods found - database empty'
    })

@api_view(['GET'])
def payment_transactions_list(request):
    """
    List payment transactions
    """
    return Response({
        'message': 'Payment transactions endpoint',
        'count': 0,
        'results': [],
        'note': 'No transactions found - database empty'
    })

@api_view(['GET'])
def exchange_rates_list(request):
    """
    List exchange rates
    """
    return Response({
        'message': 'Exchange rates endpoint',
        'count': 0,
        'results': [],
        'note': 'No exchange rates found - database empty'
    })
