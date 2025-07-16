from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """
    MayTheToken API Root - Available endpoints
    """
    return Response({
        'message': 'MTT Gateway - MayTheToken API',
        'version': '1.0',
        'endpoints': {
            'trading_pairs': '/api/maythetoken/pairs/',
            'orders': '/api/maythetoken/orders/',
            'liquidity': '/api/maythetoken/liquidity/',
            'routing': '/api/maythetoken/routing/',
        },
        'description': 'Token trading, routing engine, and liquidity management',
        'status': 'Active'
    })

@api_view(['GET'])
def trading_pairs(request):
    """
    Trading pairs endpoint
    """
    return Response({
        'message': 'Trading pairs endpoint',
        'status': 'Available',
        'count': 0,
        'results': [],
        'note': 'No trading pairs found - database empty'
    })

@api_view(['GET'])
def trade_orders(request):
    """
    Trade orders endpoint
    """
    return Response({
        'message': 'Trade orders endpoint',
        'status': 'Available',
        'count': 0,
        'results': [],
        'note': 'No orders found - database empty'
    })

@api_view(['GET'])
def liquidity_pools(request):
    """
    Liquidity pools endpoint
    """
    return Response({
        'message': 'Liquidity pools endpoint',
        'status': 'Available',
        'count': 0,
        'results': [],
        'note': 'No liquidity pools found - database empty'
    })

@api_view(['GET'])
def routing_engine(request):
    """
    Routing engine endpoint
    """
    return Response({
        'message': 'Routing engine endpoint',
        'status': 'Available',
        'engine_status': 'Online',
        'note': 'Routing engine is operational'
    })
