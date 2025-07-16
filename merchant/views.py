from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Merchant, MerchantGateway, MerchantProduct, MerchantTransaction

@api_view(['GET'])
def api_root(request):
    """
    Merchant API Root - Available endpoints
    """
    return Response({
        'message': 'MTT Gateway - Merchant API',
        'version': '1.0',
        'endpoints': {
            'merchants': '/api/merchant/list/',
            'gateways': '/api/merchant/gateways/',
            'products': '/api/merchant/products/',
            'transactions': '/api/merchant/transactions/',
        },
        'description': 'Business accounts, payment gateways, and product management'
    })

@api_view(['GET'])
def merchants_list(request):
    """
    List all merchants
    """
    merchants = Merchant.objects.all()[:10]
    data = []
    for merchant in merchants:
        data.append({
            'id': merchant.id,
            'merchant_id': str(merchant.merchant_id),
            'business_name': merchant.business_name,
            'contact_email': merchant.contact_email,
            'phone_number': merchant.phone_number,
            'verification_status': merchant.verification_status,
            'is_active': merchant.is_active,
            'created_at': merchant.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def merchant_gateways_list(request):
    """
    List merchant gateways
    """
    gateways = MerchantGateway.objects.all()[:10]
    data = []
    for gateway in gateways:
        data.append({
            'id': gateway.id,
            'gateway_id': str(gateway.gateway_id),
            'merchant_id': str(gateway.merchant.merchant_id) if gateway.merchant else None,
            'gateway_name': gateway.gateway_name,
            'gateway_type': gateway.gateway_type,
            'is_active': gateway.is_active,
            'created_at': gateway.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def merchant_products_list(request):
    """
    List merchant products
    """
    products = MerchantProduct.objects.all()[:10]
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'product_id': str(product.product_id),
            'merchant_id': str(product.merchant.merchant_id) if product.merchant else None,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'currency': product.currency,
            'is_active': product.is_active
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def merchant_transactions_list(request):
    """
    List merchant transactions
    """
    transactions = MerchantTransaction.objects.all()[:10]
    data = []
    for tx in transactions:
        data.append({
            'id': tx.id,
            'transaction_id': str(tx.transaction_id),
            'merchant_id': str(tx.merchant.merchant_id) if tx.merchant else None,
            'amount': str(tx.amount),
            'currency': tx.currency,
            'status': tx.status,
            'transaction_type': tx.transaction_type,
            'created_at': tx.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })
