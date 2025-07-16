from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class WalletType(models.Model):
    """Wallet type definitions (custodial, non-custodial, etc.)"""
    WALLET_CATEGORIES = [
        ('CUSTODIAL', 'Custodial'),
        ('NON_CUSTODIAL', 'Non-Custodial'),
        ('HYBRID', 'Hybrid'),
        ('SMART_CONTRACT', 'Smart Contract'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=WALLET_CATEGORIES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    supports_mtt = models.BooleanField(default=True)
    requires_kyc = models.BooleanField(default=False)
    min_balance = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    max_balance = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallets_type'
        verbose_name = 'Wallet Type'
        verbose_name_plural = 'Wallet Types'
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class Wallet(models.Model):
    """User wallets for MTT tokens"""
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
        ('LOCKED', 'Locked'),
        ('CLOSED', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    wallet_type = models.ForeignKey(WalletType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=42, unique=True)
    private_key_encrypted = models.TextField(null=True, blank=True)  # Encrypted for custodial wallets
    public_key = models.CharField(max_length=132, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    is_primary = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_gateway = models.BooleanField(default=False)
    backup_phrase_encrypted = models.TextField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallets_wallet'
        unique_together = ['user', 'name']
        indexes = [
            models.Index(fields=['user', 'is_primary']),
            models.Index(fields=['address']),
            models.Index(fields=['status']),
            models.Index(fields=['is_merchant']),
            models.Index(fields=['is_gateway']),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure only one primary wallet per user
        if self.is_primary:
            Wallet.objects.filter(user=self.user, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.address[:10]}...)"

class WalletAddress(models.Model):
    """Additional addresses for wallet (for receiving payments, etc.)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=42, unique=True)
    label = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_change_address = models.BooleanField(default=False)
    derivation_path = models.CharField(max_length=100, null=True, blank=True)
    address_index = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wallets_address'
        indexes = [
            models.Index(fields=['wallet', 'is_active']),
            models.Index(fields=['address']),
            models.Index(fields=['is_change_address']),
        ]
    
    def __str__(self):
        return f"{self.wallet.name} - {self.address[:10]}..."

class WalletTransaction(models.Model):
    """Wallet transaction history"""
    TRANSACTION_TYPES = [
        ('SEND', 'Send'),
        ('RECEIVE', 'Receive'),
        ('INTERNAL', 'Internal Transfer'),
        ('CONTRACT', 'Contract Interaction'),
        ('FEE', 'Fee Payment'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
        ('DROPPED', 'Dropped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_hash = models.CharField(max_length=66, unique=True)
    from_address = models.CharField(max_length=42)
    to_address = models.CharField(max_length=42)
    amount = models.DecimalField(
        max_digits=40, 
        decimal_places=18,
        validators=[MinValueValidator(Decimal('0'))]
    )
    fee = models.DecimalField(
        max_digits=40, 
        decimal_places=18,
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    gas_limit = models.PositiveBigIntegerField(null=True, blank=True)
    gas_used = models.PositiveBigIntegerField(null=True, blank=True)
    gas_price = models.PositiveBigIntegerField(null=True, blank=True)
    nonce = models.PositiveBigIntegerField(null=True, blank=True)
    block_number = models.PositiveBigIntegerField(null=True, blank=True)
    block_hash = models.CharField(max_length=66, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    confirmations = models.PositiveIntegerField(default=0)
    raw_transaction = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'wallets_transaction'
        indexes = [
            models.Index(fields=['wallet', 'created_at']),
            models.Index(fields=['transaction_hash']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['from_address']),
            models.Index(fields=['to_address']),
            models.Index(fields=['block_number']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_hash[:10]}... - {self.amount} MTT"

class WalletBackup(models.Model):
    """Wallet backup information"""
    BACKUP_TYPES = [
        ('SEED_PHRASE', 'Seed Phrase'),
        ('PRIVATE_KEY', 'Private Key'),
        ('KEYSTORE', 'Keystore File'),
        ('HARDWARE', 'Hardware Wallet'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='backups')
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPES)
    encrypted_data = models.TextField()  # Encrypted backup data
    checksum = models.CharField(max_length=64)  # SHA-256 checksum
    is_verified = models.BooleanField(default=False)
    last_verified = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallets_backup'
        unique_together = ['wallet', 'backup_type']
        indexes = [
            models.Index(fields=['wallet', 'backup_type']),
            models.Index(fields=['is_verified']),
        ]
    
    def __str__(self):
        return f"{self.wallet.name} - {self.backup_type}"

class WalletPermission(models.Model):
    """Wallet access permissions for different users/roles"""
    PERMISSION_TYPES = [
        ('READ', 'Read Only'),
        ('SEND', 'Send Transactions'),
        ('MANAGE', 'Full Management'),
        ('ADMIN', 'Administrative Access'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPES)
    granted_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='granted_permissions'
    )
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wallets_permission'
        unique_together = ['wallet', 'user', 'permission_type']
        indexes = [
            models.Index(fields=['wallet', 'user']),
            models.Index(fields=['user', 'permission_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.wallet.name} ({self.permission_type})"
