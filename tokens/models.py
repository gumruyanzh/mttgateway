from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Token(models.Model):
    """MTT Token configuration and metadata"""
    name = models.CharField(max_length=100, default='MayTheToken')
    symbol = models.CharField(max_length=10, default='MTT')
    decimals = models.PositiveIntegerField(default=18)
    total_supply = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    contract_address = models.CharField(max_length=42, unique=True)
    chain_id = models.PositiveIntegerField(default=1)  # Ethereum mainnet
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tokens_token'
        verbose_name = 'MTT Token'
        verbose_name_plural = 'MTT Tokens'
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"

class TokenBalance(models.Model):
    """User MTT token balances"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='token_balances')
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    locked_balance = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    available_balance = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tokens_balance'
        unique_together = ['user', 'token']
        indexes = [
            models.Index(fields=['user', 'token']),
            models.Index(fields=['balance']),
        ]
    
    def save(self, *args, **kwargs):
        # Calculate available balance
        self.available_balance = max(Decimal('0'), self.balance - self.locked_balance)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.balance} {self.token.symbol}"

class TokenTransfer(models.Model):
    """MTT token transfer records"""
    TRANSFER_TYPES = [
        ('SEND', 'Send'),
        ('RECEIVE', 'Receive'),
        ('PURCHASE', 'Purchase'),
        ('SALE', 'Sale'),
        ('REWARD', 'Reward'),
        ('REFUND', 'Refund'),
        ('FEE', 'Fee'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    from_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='token_transfers_sent',
        null=True, 
        blank=True
    )
    to_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='token_transfers_received',
        null=True, 
        blank=True
    )
    from_address = models.CharField(max_length=42, null=True, blank=True)
    to_address = models.CharField(max_length=42, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=40, 
        decimal_places=18,
        validators=[MinValueValidator(Decimal('0.000000000000000001'))]
    )
    transaction_hash = models.CharField(max_length=66, unique=True, null=True, blank=True)
    block_number = models.PositiveBigIntegerField(null=True, blank=True)
    gas_used = models.PositiveBigIntegerField(null=True, blank=True)
    gas_price = models.PositiveBigIntegerField(null=True, blank=True)
    transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'tokens_transfer'
        indexes = [
            models.Index(fields=['from_user', 'created_at']),
            models.Index(fields=['to_user', 'created_at']),
            models.Index(fields=['transaction_hash']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['transfer_type']),
        ]
    
    def __str__(self):
        return f"{self.amount} {self.token.symbol} - {self.transfer_type}"

class TokenPrice(models.Model):
    """MTT token price tracking"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    price_usd = models.DecimalField(max_digits=20, decimal_places=8)
    price_eth = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    market_cap = models.DecimalField(max_digits=40, decimal_places=2, null=True, blank=True)
    volume_24h = models.DecimalField(max_digits=40, decimal_places=2, null=True, blank=True)
    source = models.CharField(max_length=50, default='internal')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tokens_price'
        indexes = [
            models.Index(fields=['token', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.token.symbol} - ${self.price_usd}"

class TokenAllowance(models.Model):
    """Token allowances for smart contract interactions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    spender_address = models.CharField(max_length=42)
    allowance = models.DecimalField(
        max_digits=40, 
        decimal_places=18,
        validators=[MinValueValidator(Decimal('0'))]
    )
    transaction_hash = models.CharField(max_length=66, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tokens_allowance'
        unique_together = ['token', 'owner', 'spender_address']
        indexes = [
            models.Index(fields=['owner', 'spender_address']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.owner.username} -> {self.spender_address}: {self.allowance}"
