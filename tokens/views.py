from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Token, TokenBalance, TokenTransfer, TokenPrice

# Create your views here.

@api_view(['GET'])
def api_root(request):
    """
    Tokens API Root - Available endpoints
    """
    return Response({
        'message': 'MTT Gateway - Tokens API',
        'version': '1.0',
        'endpoints': {
            'tokens': '/api/tokens/list/',
            'balances': '/api/tokens/balances/',
            'transfers': '/api/tokens/transfers/',
            'prices': '/api/tokens/prices/',
        },
        'description': 'MTT token management, balances, transfers, and pricing system'
    })

@api_view(['GET'])
def tokens_list(request):
    """
    List all tokens
    """
    tokens = Token.objects.all()[:10]
    data = []
    for token in tokens:
        data.append({
            'id': token.id,
            'token_id': str(token.token_id),
            'name': token.name,
            'symbol': token.symbol,
            'total_supply': str(token.total_supply),
            'decimals': token.decimals,
            'contract_address': token.contract_address,
            'blockchain': token.blockchain,
            'is_active': token.is_active,
            'created_at': token.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def token_balances_list(request):
    """
    List token balances
    """
    balances = TokenBalance.objects.all()[:10]
    data = []
    for balance in balances:
        data.append({
            'id': balance.id,
            'user_id': balance.user.id if balance.user else None,
            'username': balance.user.username if balance.user else None,
            'token_symbol': balance.token.symbol if balance.token else None,
            'balance': str(balance.balance),
            'locked_balance': str(balance.locked_balance),
            'updated_at': balance.updated_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def token_transfers_list(request):
    """
    List token transfers
    """
    transfers = TokenTransfer.objects.all()[:10]
    data = []
    for transfer in transfers:
        data.append({
            'id': transfer.id,
            'transfer_id': str(transfer.transfer_id),
            'token_symbol': transfer.token.symbol if transfer.token else None,
            'from_user': transfer.from_user.username if transfer.from_user else None,
            'to_user': transfer.to_user.username if transfer.to_user else None,
            'amount': str(transfer.amount),
            'status': transfer.status,
            'created_at': transfer.created_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })

@api_view(['GET'])
def token_prices_list(request):
    """
    List token prices
    """
    prices = TokenPrice.objects.all()[:10]
    data = []
    for price in prices:
        data.append({
            'id': price.id,
            'token_symbol': price.token.symbol if price.token else None,
            'price_usd': str(price.price_usd),
            'source': price.source,
            'updated_at': price.updated_at.isoformat()
        })
    
    return Response({
        'count': len(data),
        'results': data
    })
