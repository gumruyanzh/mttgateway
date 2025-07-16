"""
WebSocket routing configuration for mtt_gateway project.
Handles real-time connections for payment notifications, wallet updates, etc.
"""

from django.urls import path
from channels.routing import URLRouter

# Import consumers from each app when available
# from payments.consumers import PaymentConsumer
# from wallets.consumers import WalletConsumer
# from maythetoken.consumers import TradingConsumer

websocket_urlpatterns = [
    # Real-time payment notifications
    # path('ws/payments/', PaymentConsumer.as_asgi()),
    
    # Real-time wallet updates
    # path('ws/wallets/', WalletConsumer.as_asgi()),
    
    # Real-time trading updates
    # path('ws/trading/', TradingConsumer.as_asgi()),
    
    # Placeholder - will be updated when consumers are implemented
] 