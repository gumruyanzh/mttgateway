from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

class TradingPair(models.Model):
    """Trading pairs for MTT token"""
    base_currency = models.CharField(max_length=10)  # MTT
    quote_currency = models.CharField(max_length=10)  # USD, ETH, BTC, etc.
    symbol = models.CharField(max_length=20, unique=True)  # MTT/USD
    is_active = models.BooleanField(default=True)
    
    # Trading limits
    min_order_size = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        default=1,
        validators=[MinValueValidator(Decimal('0.000000000000000001'))]
    )
    max_order_size = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.000000000000000001'))]
    )
    
    # Trading fees
    maker_fee = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('0.1'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    taker_fee = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('0.2'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'maythetoken_trading_pair'
        unique_together = ['base_currency', 'quote_currency']
    
    def __str__(self):
        return self.symbol

class TradeOrder(models.Model):
    """Trading orders for MTT tokens"""
    ORDER_TYPES = [
        ('MARKET', 'Market Order'),
        ('LIMIT', 'Limit Order'),
        ('STOP', 'Stop Order'),
        ('STOP_LIMIT', 'Stop Limit Order'),
    ]
    
    SIDES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('OPEN', 'Open'),
        ('PARTIALLY_FILLED', 'Partially Filled'),
        ('FILLED', 'Filled'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_orders')
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE)
    
    # Order details
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES)
    side = models.CharField(max_length=10, choices=SIDES)
    quantity = models.DecimalField(
        max_digits=40, 
        decimal_places=18,
        validators=[MinValueValidator(Decimal('0.000000000000000001'))]
    )
    price = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        null=True, 
        blank=True  # null for market orders
    )
    stop_price = models.DecimalField(
        max_digits=20, 
        decimal_places=8, 
        null=True, 
        blank=True
    )
    
    # Execution details
    filled_quantity = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    remaining_quantity = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    average_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    total_value = models.DecimalField(max_digits=40, decimal_places=8, default=0)
    
    # Fees
    commission = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    commission_asset = models.CharField(max_length=10, default='MTT')
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    time_in_force = models.CharField(
        max_length=10, 
        choices=[
            ('GTC', 'Good Till Cancelled'),
            ('IOC', 'Immediate or Cancel'),
            ('FOK', 'Fill or Kill'),
        ], 
        default='GTC'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'maythetoken_trade_order'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['trading_pair', 'side', 'price']),
            models.Index(fields=['status', 'created_at']),
        ]
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        self.remaining_quantity = self.quantity - self.filled_quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.side} {self.quantity} {self.trading_pair.symbol} @ {self.price}"

class TradeExecution(models.Model):
    """Individual trade executions/fills"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buy_order = models.ForeignKey(TradeOrder, on_delete=models.CASCADE, related_name='buy_executions')
    sell_order = models.ForeignKey(TradeOrder, on_delete=models.CASCADE, related_name='sell_executions')
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE)
    
    # Execution details
    quantity = models.DecimalField(
        max_digits=40, 
        decimal_places=18,
        validators=[MinValueValidator(Decimal('0.000000000000000001'))]
    )
    price = models.DecimalField(max_digits=20, decimal_places=8)
    total_value = models.DecimalField(max_digits=40, decimal_places=8)
    
    # Fees
    buyer_fee = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    seller_fee = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    
    executed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'maythetoken_trade_execution'
        indexes = [
            models.Index(fields=['trading_pair', 'executed_at']),
            models.Index(fields=['buy_order']),
            models.Index(fields=['sell_order']),
        ]
        ordering = ['-executed_at']
    
    def __str__(self):
        return f"{self.quantity} {self.trading_pair.symbol} @ {self.price}"

class TokenIssuance(models.Model):
    """MTT token issuance records"""
    ISSUANCE_TYPES = [
        ('INITIAL', 'Initial Issuance'),
        ('REWARD', 'Reward Issuance'),
        ('BONUS', 'Bonus Issuance'),
        ('BURN', 'Token Burn'),
        ('MINT', 'Additional Mint'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey('tokens.Token', on_delete=models.CASCADE, related_name='issuances')
    
    # Issuance details
    issuance_type = models.CharField(max_length=20, choices=ISSUANCE_TYPES)
    amount = models.DecimalField(
        max_digits=40, 
        decimal_places=18,
        validators=[MinValueValidator(Decimal('0.000000000000000001'))]
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    recipient_address = models.CharField(max_length=42, null=True, blank=True)
    
    # Blockchain details
    transaction_hash = models.CharField(max_length=66, unique=True, null=True, blank=True)
    block_number = models.PositiveBigIntegerField(null=True, blank=True)
    gas_used = models.PositiveBigIntegerField(null=True, blank=True)
    
    # Authorization
    authorized_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authorized_issuances')
    authorization_signature = models.TextField(null=True, blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'maythetoken_issuance'
        indexes = [
            models.Index(fields=['token', 'issuance_type']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['recipient']),
            models.Index(fields=['authorized_by']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.issuance_type} - {self.amount} MTT"

class RoutingEngine(models.Model):
    """Payment routing engine configuration"""
    ROUTING_STRATEGIES = [
        ('DIRECT', 'Direct Transfer'),
        ('MULTI_HOP', 'Multi-hop Routing'),
        ('LIQUIDITY_BASED', 'Liquidity-based Routing'),
        ('COST_OPTIMIZED', 'Cost Optimized'),
        ('SPEED_OPTIMIZED', 'Speed Optimized'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    strategy = models.CharField(max_length=20, choices=ROUTING_STRATEGIES)
    
    # Configuration parameters
    max_hops = models.PositiveSmallIntegerField(default=3)
    max_routing_time_seconds = models.PositiveIntegerField(default=30)
    min_liquidity_threshold = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        default=1000,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    # Fee parameters
    base_routing_fee = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('0.05'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    hop_fee_multiplier = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=Decimal('1.5'),
        validators=[MinValueValidator(Decimal('1'))]
    )
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    is_default = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(default=100)
    
    # Performance metrics
    success_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    average_routing_time = models.DurationField(null=True, blank=True)
    total_volume_routed = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'maythetoken_routing_engine'
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['is_default']),
            models.Index(fields=['strategy']),
        ]
        ordering = ['priority', '-success_rate']
    
    def __str__(self):
        return f"{self.name} ({self.strategy})"

class RoutingPath(models.Model):
    """Individual routing paths used by the routing engine"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    routing_engine = models.ForeignKey(RoutingEngine, on_delete=models.CASCADE, related_name='routing_paths')
    
    # Path details
    from_address = models.CharField(max_length=42)
    to_address = models.CharField(max_length=42)
    intermediate_addresses = models.JSONField(default=list)  # List of intermediate addresses
    path_length = models.PositiveSmallIntegerField()  # Number of hops
    
    # Performance metrics
    estimated_cost = models.DecimalField(max_digits=40, decimal_places=18)
    estimated_time_seconds = models.PositiveIntegerField()
    liquidity_score = models.PositiveSmallIntegerField(default=0)  # 0-100
    
    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    failure_count = models.PositiveIntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'maythetoken_routing_path'
        unique_together = ['routing_engine', 'from_address', 'to_address']
        indexes = [
            models.Index(fields=['routing_engine', 'is_active']),
            models.Index(fields=['from_address', 'to_address']),
            models.Index(fields=['liquidity_score']),
        ]
    
    @property
    def success_rate(self):
        if self.usage_count == 0:
            return 0
        return (self.success_count / self.usage_count) * 100
    
    def __str__(self):
        return f"{self.from_address[:10]}...→{self.to_address[:10]}... ({self.path_length} hops)"

class LiquidityPool(models.Model):
    """Liquidity pools for MTT token trading"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='liquidity_pools')
    
    # Pool details
    name = models.CharField(max_length=100)
    pool_address = models.CharField(max_length=42, unique=True)
    
    # Liquidity amounts
    base_reserve = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    quote_reserve = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    total_liquidity = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    
    # Pool parameters
    fee_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('0.3'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    
    # Status and metrics
    is_active = models.BooleanField(default=True)
    volume_24h = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    fees_earned_24h = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'maythetoken_liquidity_pool'
        unique_together = ['trading_pair', 'name']
        indexes = [
            models.Index(fields=['trading_pair', 'is_active']),
            models.Index(fields=['pool_address']),
            models.Index(fields=['total_liquidity']),
        ]
    
    @property
    def price(self):
        if self.base_reserve == 0:
            return 0
        return self.quote_reserve / self.base_reserve
    
    def __str__(self):
        return f"{self.name} - {self.trading_pair.symbol}"
