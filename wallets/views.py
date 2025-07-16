from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import WalletType, Wallet, WalletAddress, WalletTransaction

@api_view(['GET'])
def api_root(request):
    """
    Wallets API Root - Available endpoints
    """
    return Response({
        'message': 'MTT Gateway - Wallets API',
        'version': '1.0',
        'endpoints': {
            'wallet_types': '/api/wallets/types/',
            'wallets': '/api/wallets/list/',
            'addresses': '/api/wallets/addresses/',
            'transactions': '/api/wallets/transactions/',
        },
        'description': 'Custodial and non-custodial wallet management with security features'
    })

@api_view(['GET', 'POST'])
def wallet_types_list(request):
    """
    List all wallet types or create a new one
    """
    if request.method == 'GET':
        wallet_types = WalletType.objects.all()
        data = []
        for wt in wallet_types:
            data.append({
                'id': wt.id,
                'name': wt.name,
                'description': wt.description,
                'is_custodial': wt.is_custodial,
                'security_level': wt.security_level,
                'created_at': wt.created_at.isoformat()
            })
        return Response({
            'count': len(data),
            'results': data
        })
    
    elif request.method == 'POST':
        # Create new wallet type
        return Response({
            'message': 'POST method for creating wallet types',
            'note': 'Implementation would create new wallet type here'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def wallets_list(request):
    """
    List all wallets or create a new one
    """
    if request.method == 'GET':
        wallets = Wallet.objects.all()[:10]  # Limit to 10 for demo
        data = []
        for wallet in wallets:
            data.append({
                'id': wallet.id,
                'wallet_id': str(wallet.wallet_id),
                'user_id': wallet.user.id if wallet.user else None,
                'username': wallet.user.username if wallet.user else None,
                'wallet_type': wallet.wallet_type.name if wallet.wallet_type else None,
                'balance': str(wallet.balance),
                'currency': wallet.currency,
                'is_active': wallet.is_active,
                'created_at': wallet.created_at.isoformat()
            })
        return Response({
            'count': len(data),
            'results': data
        })
    
    elif request.method == 'POST':
        return Response({
            'message': 'POST method for creating wallets',
            'note': 'Implementation would create new wallet here'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def wallet_addresses_list(request):
    """
    List wallet addresses
    """
    addresses = WalletAddress.objects.all()[:10]
    data = []
    for addr in addresses:
        data.append({
            'id': addr.id,
            'wallet_id': str(addr.wallet.wallet_id) if addr.wallet else None,
            'address': addr.address,
            'blockchain': addr.blockchain,
            'address_type': addr.address_type,
            'is_active': addr.is_active,
            'created_at': addr.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def wallet_transactions_list(request):
    """
    List wallet transactions
    """
    transactions = WalletTransaction.objects.all()[:10]
    data = []
    for tx in transactions:
        data.append({
            'id': tx.id,
            'transaction_id': str(tx.transaction_id),
            'wallet_id': str(tx.wallet.wallet_id) if tx.wallet else None,
            'transaction_type': tx.transaction_type,
            'amount': str(tx.amount),
            'currency': tx.currency,
            'status': tx.status,
            'created_at': tx.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })
