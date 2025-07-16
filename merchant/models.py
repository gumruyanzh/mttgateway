from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

class MerchantCategory(models.Model):
    """Merchant business categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low Risk'),
            ('MEDIUM', 'Medium Risk'),
            ('HIGH', 'High Risk'),
        ],
        default='MEDIUM'
    )
    requires_verification = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'merchant_category'
        verbose_name = 'Merchant Category'
        verbose_name_plural = 'Merchant Categories'
    
    def __str__(self):
        return self.name

class Merchant(models.Model):
    """Merchant account information"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('INACTIVE', 'Inactive'),
        ('TERMINATED', 'Terminated'),
    ]
    
    VERIFICATION_LEVELS = [
        ('NONE', 'No Verification'),
        ('BASIC', 'Basic Verification'),
        ('ENHANCED', 'Enhanced Verification'),
        ('PREMIUM', 'Premium Verification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant_profile')
    business_name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200, null=True, blank=True)
    business_registration_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    tax_id = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(MerchantCategory, on_delete=models.CASCADE)
    website_url = models.URLField(null=True, blank=True)
    support_email = models.EmailField()
    support_phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Address information
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=2)  # ISO country code
    
    # Status and verification
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    verification_level = models.CharField(max_length=20, choices=VERIFICATION_LEVELS, default='NONE')
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verified_merchants'
    )
    
    # Business metrics
    monthly_volume_limit = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=10000,
        validators=[MinValueValidator(Decimal('0'))]
    )
    transaction_limit = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=1000,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'merchant_merchant'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['business_name']),
        ]
    
    def __str__(self):
        return f"{self.business_name} ({self.user.username})"

class MerchantGateway(models.Model):
    """Merchant gateway wallet configurations"""
    GATEWAY_TYPES = [
        ('CUSTODIAL', 'Custodial Gateway'),
        ('NON_CUSTODIAL', 'Non-Custodial Gateway'),
        ('HYBRID', 'Hybrid Gateway'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Maintenance'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='gateways')
    name = models.CharField(max_length=100)
    gateway_type = models.CharField(max_length=20, choices=GATEWAY_TYPES)
    wallet_address = models.CharField(max_length=42, unique=True)
    encrypted_private_key = models.TextField(null=True, blank=True)  # For custodial
    
    # Configuration
    auto_settlement = models.BooleanField(default=True)
    settlement_threshold = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        default=100,
        validators=[MinValueValidator(Decimal('0'))]
    )
    callback_url = models.URLField(null=True, blank=True)
    webhook_secret = models.CharField(max_length=64, null=True, blank=True)
    
    # Fee structure
    transaction_fee_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('0.5'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    flat_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    is_primary = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'merchant_gateway'
        unique_together = ['merchant', 'name']
        indexes = [
            models.Index(fields=['merchant', 'status']),
            models.Index(fields=['wallet_address']),
            models.Index(fields=['is_primary']),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure only one primary gateway per merchant
        if self.is_primary:
            MerchantGateway.objects.filter(merchant=self.merchant, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.merchant.business_name} - {self.name}"

class MerchantProduct(models.Model):
    """Products/services offered by merchants"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    price_usd = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    price_mtt = models.DecimalField(
        max_digits=40, 
        decimal_places=18,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.000000000000000001'))]
    )
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(null=True, blank=True)  # null = unlimited
    track_inventory = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    category = models.CharField(max_length=100, blank=True)
    tags = models.TextField(blank=True)  # JSON array of tags
    image_url = models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'merchant_product'
        unique_together = ['merchant', 'sku']
        indexes = [
            models.Index(fields=['merchant', 'is_active']),
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return f"{self.merchant.business_name} - {self.name}"

class MerchantApiKey(models.Model):
    """API keys for merchant integration"""
    ENVIRONMENT_CHOICES = [
        ('SANDBOX', 'Sandbox'),
        ('PRODUCTION', 'Production'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=64, unique=True)
    api_secret = models.CharField(max_length=128)
    environment = models.CharField(max_length=20, choices=ENVIRONMENT_CHOICES)
    
    # Permissions
    can_read = models.BooleanField(default=True)
    can_write = models.BooleanField(default=False)
    can_refund = models.BooleanField(default=False)
    
    # Rate limiting
    rate_limit_per_minute = models.PositiveIntegerField(default=60)
    rate_limit_per_hour = models.PositiveIntegerField(default=3600)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'merchant_api_key'
        unique_together = ['merchant', 'name', 'environment']
        indexes = [
            models.Index(fields=['api_key']),
            models.Index(fields=['merchant', 'is_active']),
            models.Index(fields=['environment']),
        ]
    
    def __str__(self):
        return f"{self.merchant.business_name} - {self.name} ({self.environment})"

class MerchantTransaction(models.Model):
    """Merchant transaction records"""
    TRANSACTION_TYPES = [
        ('PAYMENT', 'Payment'),
        ('REFUND', 'Refund'),
        ('SETTLEMENT', 'Settlement'),
        ('FEE', 'Fee'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='transactions')
    gateway = models.ForeignKey(MerchantGateway, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(MerchantProduct, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Transaction details
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount_usd = models.DecimalField(max_digits=15, decimal_places=2)
    amount_mtt = models.DecimalField(max_digits=40, decimal_places=18)
    fee_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Blockchain details
    transaction_hash = models.CharField(max_length=66, null=True, blank=True)
    from_address = models.CharField(max_length=42, null=True, blank=True)
    to_address = models.CharField(max_length=42, null=True, blank=True)
    
    # Customer information
    customer_email = models.EmailField(null=True, blank=True)
    customer_reference = models.CharField(max_length=100, null=True, blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reference_id = models.CharField(max_length=100, null=True, blank=True)  # Merchant's reference
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'merchant_transaction'
        indexes = [
            models.Index(fields=['merchant', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['transaction_hash']),
            models.Index(fields=['reference_id']),
            models.Index(fields=['customer_email']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.merchant.business_name} - ${self.amount_usd} ({self.status})"
