from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

class Marketplace(models.Model):
    """Marketplace configuration and settings"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='marketplace_logos/', null=True, blank=True)
    
    # Configuration
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('2.5'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    min_listing_price = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=1,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    max_listing_price = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=True)
    allow_external_sellers = models.BooleanField(default=True)
    
    # Supported currencies
    supported_currencies = models.JSONField(default=list)  # ['USD', 'EUR', 'MTT']
    default_currency = models.CharField(max_length=3, default='USD')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'weedvader_marketplace'
    
    def __str__(self):
        return self.name

class MarketplaceListing(models.Model):
    """Items listed on the marketplace"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Approval'),
        ('ACTIVE', 'Active'),
        ('SOLD', 'Sold'),
        ('SUSPENDED', 'Suspended'),
        ('EXPIRED', 'Expired'),
    ]
    
    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('LIKE_NEW', 'Like New'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE, related_name='listings')
    seller = models.ForeignKey('merchant.Merchant', on_delete=models.CASCADE, related_name='marketplace_listings')
    
    # Product information
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='NEW')
    
    # Pricing
    price_usd = models.DecimalField(
        max_digits=15, 
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
    quantity = models.PositiveIntegerField(default=1)
    sku = models.CharField(max_length=100, blank=True)
    
    # Images and media
    primary_image = models.ImageField(upload_to='marketplace_listings/', null=True, blank=True)
    additional_images = models.JSONField(default=list, blank=True)  # List of image URLs
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    favorites_count = models.PositiveIntegerField(default=0)
    
    # SEO
    slug = models.SlugField(max_length=250, unique=True)
    meta_description = models.CharField(max_length=160, blank=True)
    tags = models.JSONField(default=list, blank=True)  # List of tags
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'weedvader_marketplace_listing'
        indexes = [
            models.Index(fields=['marketplace', 'status']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - ${self.price_usd}"

class MarketplaceOrder(models.Model):
    """Orders placed on the marketplace"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Paid'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
        ('DISPUTED', 'Disputed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE)
    listing = models.ForeignKey(MarketplaceListing, on_delete=models.CASCADE)
    buyer = models.ForeignKey('customers.CustomerProfile', on_delete=models.CASCADE, related_name='marketplace_orders')
    seller = models.ForeignKey('merchant.Merchant', on_delete=models.CASCADE, related_name='marketplace_sales')
    
    # Order details
    quantity = models.PositiveIntegerField(default=1)
    unit_price_usd = models.DecimalField(max_digits=15, decimal_places=2)
    unit_price_mtt = models.DecimalField(max_digits=40, decimal_places=18, null=True, blank=True)
    total_amount_usd = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount_mtt = models.DecimalField(max_digits=40, decimal_places=18, null=True, blank=True)
    
    # Fees
    marketplace_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payment_processing_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    seller_net_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Shipping
    shipping_address = models.JSONField(default=dict, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tracking_number = models.CharField(max_length=100, blank=True)
    shipping_carrier = models.CharField(max_length=50, blank=True)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    order_number = models.CharField(max_length=20, unique=True)
    
    # Payment reference
    payment_transaction = models.ForeignKey(
        'payments.PaymentTransaction', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'weedvader_marketplace_order'
        indexes = [
            models.Index(fields=['buyer', 'status']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['marketplace', 'created_at']),
            models.Index(fields=['order_number']),
            models.Index(fields=['status', 'created_at']),
        ]
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            import random
            import string
            self.order_number = 'MKT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order_number} - {self.listing.title}"

class CardPaymentProcessor(models.Model):
    """Card payment processor configurations"""
    PROCESSOR_TYPES = [
        ('STRIPE', 'Stripe'),
        ('PAYPAL', 'PayPal'),
        ('SQUARE', 'Square'),
        ('ADYEN', 'Adyen'),
        ('AUTHORIZE_NET', 'Authorize.Net'),
        ('BRAINTREE', 'Braintree'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('TESTING', 'Testing'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    processor_type = models.CharField(max_length=20, choices=PROCESSOR_TYPES)
    
    # API Configuration
    api_endpoint = models.URLField()
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    webhook_secret = models.CharField(max_length=255, null=True, blank=True)
    
    # Supported features
    supports_cards = models.BooleanField(default=True)
    supports_digital_wallets = models.BooleanField(default=False)
    supports_bank_transfers = models.BooleanField(default=False)
    supports_subscriptions = models.BooleanField(default=False)
    
    # Fee structure
    transaction_fee_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=Decimal('2.9'),
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    fixed_fee_cents = models.PositiveIntegerField(default=30)  # in cents
    
    # Limits and settings
    min_transaction_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=1,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    max_transaction_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INACTIVE')
    is_default = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(default=100)
    
    # Performance metrics
    success_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    average_processing_time = models.DurationField(null=True, blank=True)
    total_volume_processed = models.DecimalField(max_digits=40, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'weedvader_card_processor'
        indexes = [
            models.Index(fields=['processor_type']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['is_default']),
        ]
        ordering = ['priority', '-success_rate']
    
    def __str__(self):
        return f"{self.name} ({self.processor_type})"

class BankProcessor(models.Model):
    """Bank payment processor for fiat transactions"""
    BANK_TYPES = [
        ('COMMERCIAL', 'Commercial Bank'),
        ('INVESTMENT', 'Investment Bank'),
        ('CENTRAL', 'Central Bank'),
        ('CREDIT_UNION', 'Credit Union'),
        ('ONLINE', 'Online Bank'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('UNDER_REVIEW', 'Under Review'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bank_name = models.CharField(max_length=200)
    bank_code = models.CharField(max_length=20, unique=True)  # SWIFT/BIC code
    bank_type = models.CharField(max_length=20, choices=BANK_TYPES)
    country = models.CharField(max_length=2)  # ISO country code
    
    # Connection details
    api_endpoint = models.URLField(null=True, blank=True)
    connection_type = models.CharField(
        max_length=20,
        choices=[
            ('API', 'API Integration'),
            ('SFTP', 'SFTP'),
            ('MANUAL', 'Manual Processing'),
        ],
        default='API'
    )
    
    # Processing capabilities
    supports_instant_transfer = models.BooleanField(default=False)
    supports_batch_transfer = models.BooleanField(default=True)
    supports_international = models.BooleanField(default=False)
    
    # Limits and fees
    daily_limit = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    per_transaction_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    percentage_fee = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=0,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    
    # Processing times
    domestic_processing_hours = models.PositiveIntegerField(default=24)
    international_processing_hours = models.PositiveIntegerField(default=72)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INACTIVE')
    is_primary = models.BooleanField(default=False)
    
    # Performance tracking
    total_transactions = models.PositiveIntegerField(default=0)
    total_volume = models.DecimalField(max_digits=40, decimal_places=2, default=0)
    success_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'weedvader_bank_processor'
        indexes = [
            models.Index(fields=['bank_code']),
            models.Index(fields=['bank_type', 'country']),
            models.Index(fields=['status']),
            models.Index(fields=['is_primary']),
        ]
    
    def __str__(self):
        return f"{self.bank_name} ({self.bank_code})"

class FiatTransaction(models.Model):
    """Fiat currency transactions processed through banks"""
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
        ('CONVERSION', 'Currency Conversion'),
        ('FEE_COLLECTION', 'Fee Collection'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
        ('REVERSED', 'Reversed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bank_processor = models.ForeignKey(BankProcessor, on_delete=models.CASCADE, related_name='transactions')
    
    # Transaction details
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reference_number = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    
    # Account details
    from_account = models.CharField(max_length=50, null=True, blank=True)
    to_account = models.CharField(max_length=50, null=True, blank=True)
    from_account_name = models.CharField(max_length=200, null=True, blank=True)
    to_account_name = models.CharField(max_length=200, null=True, blank=True)
    
    # Fees
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
    
    # Associated records
    marketplace_order = models.ForeignKey(
        MarketplaceOrder, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    payment_transaction = models.ForeignKey(
        'payments.PaymentTransaction', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    external_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    bank_confirmation_code = models.CharField(max_length=100, null=True, blank=True)
    
    # Additional information
    description = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'weedvader_fiat_transaction'
        indexes = [
            models.Index(fields=['bank_processor', 'status']),
            models.Index(fields=['reference_number']),
            models.Index(fields=['transaction_type', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['external_transaction_id']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reference_number} - {self.amount} {self.currency} ({self.status})"
