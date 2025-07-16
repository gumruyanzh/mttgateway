from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

class PaymentMethod(models.Model):
    """Payment methods supported by the system"""
    METHOD_TYPES = [
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('PAYPAL', 'PayPal'),
        ('STRIPE', 'Stripe'),
        ('MTT_TOKEN', 'MTT Token'),
        ('CRYPTO', 'Cryptocurrency'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    method_type = models.CharField(max_length=20, choices=METHOD_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_fiat = models.BooleanField(default=True)
    processing_fee_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=0,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    flat_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    min_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=1,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    max_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    settlement_time_hours = models.PositiveIntegerField(default=24)  # Settlement time in hours
    requires_kyc = models.BooleanField(default=False)
    supported_currencies = models.JSONField(default=list)  # List of supported currency codes
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments_method'
        indexes = [
            models.Index(fields=['method_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_fiat']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.method_type})"

class CustomerPaymentMethod(models.Model):
    """Customer saved payment methods"""
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('EXPIRED', 'Expired'),
        ('INVALID', 'Invalid'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('customers.CustomerProfile', on_delete=models.CASCADE, related_name='payment_methods')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    
    # Payment details (encrypted/tokenized)
    nickname = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=255)  # Payment processor token
    last_four = models.CharField(max_length=4, blank=True)  # Last 4 digits for display
    card_brand = models.CharField(max_length=20, blank=True)  # Visa, MasterCard, etc.
    expiry_month = models.PositiveSmallIntegerField(null=True, blank=True)
    expiry_year = models.PositiveIntegerField(null=True, blank=True)
    
    # Status and preferences
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    is_default = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments_customer_method'
        unique_together = ['customer', 'token']
        indexes = [
            models.Index(fields=['customer', 'is_default']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_method']),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure only one default payment method per customer
        if self.is_default:
            CustomerPaymentMethod.objects.filter(customer=self.customer, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.customer.user.username} - {self.payment_method.name} ({self.last_four})"

class PaymentTransaction(models.Model):
    """Payment transaction records"""
    TRANSACTION_TYPES = [
        ('PURCHASE', 'Purchase MTT'),
        ('SALE', 'Sell MTT'),
        ('CONVERSION', 'Fiat to MTT Conversion'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('DEPOSIT', 'Deposit'),
        ('REFUND', 'Refund'),
        ('FEE', 'Fee Payment'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
        ('EXPIRED', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('customers.CustomerProfile', on_delete=models.CASCADE, related_name='payment_transactions')
    merchant = models.ForeignKey('merchant.Merchant', on_delete=models.CASCADE, null=True, blank=True, related_name='received_payments')
    payment_method = models.ForeignKey(CustomerPaymentMethod, on_delete=models.CASCADE)
    
    # Transaction details
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reference_id = models.CharField(max_length=100, unique=True)  # External reference
    
    # Amounts
    fiat_amount = models.DecimalField(max_digits=15, decimal_places=2)
    fiat_currency = models.CharField(max_length=3, default='USD')
    mtt_amount = models.DecimalField(max_digits=40, decimal_places=18)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=8)  # MTT per fiat unit
    
    # Fees
    platform_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    processing_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_fees = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # External processor details
    processor = models.CharField(max_length=50, default='stripe')  # stripe, paypal, etc.
    processor_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    processor_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    processor_response = models.JSONField(default=dict, blank=True)
    
    # Blockchain details (for MTT transactions)
    blockchain_transaction_hash = models.CharField(max_length=66, null=True, blank=True)
    from_address = models.CharField(max_length=42, null=True, blank=True)
    to_address = models.CharField(max_length=42, null=True, blank=True)
    gas_used = models.PositiveBigIntegerField(null=True, blank=True)
    gas_price = models.PositiveBigIntegerField(null=True, blank=True)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    failure_reason = models.TextField(blank=True)
    retry_count = models.PositiveSmallIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    customer_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments_transaction'
        indexes = [
            models.Index(fields=['customer', 'created_at']),
            models.Index(fields=['merchant', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['reference_id']),
            models.Index(fields=['processor_transaction_id']),
            models.Index(fields=['blockchain_transaction_hash']),
            models.Index(fields=['transaction_type']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reference_id} - {self.fiat_amount} {self.fiat_currency} to {self.mtt_amount} MTT"

class ExchangeRate(models.Model):
    """MTT token exchange rates"""
    base_currency = models.CharField(max_length=3, default='USD')
    target_currency = models.CharField(max_length=10, default='MTT')
    rate = models.DecimalField(max_digits=20, decimal_places=8)  # How many target units per base unit
    
    # Rate metadata
    source = models.CharField(max_length=50, default='internal')  # API source or manual
    bid_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    ask_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    volume_24h = models.DecimalField(max_digits=40, decimal_places=2, null=True, blank=True)
    
    # Validity
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments_exchange_rate'
        unique_together = ['base_currency', 'target_currency', 'valid_from']
        indexes = [
            models.Index(fields=['base_currency', 'target_currency', 'is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['source']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"1 {self.base_currency} = {self.rate} {self.target_currency}"

class PaymentWebhook(models.Model):
    """Payment processor webhook events"""
    WEBHOOK_TYPES = [
        ('PAYMENT_SUCCESS', 'Payment Successful'),
        ('PAYMENT_FAILED', 'Payment Failed'),
        ('REFUND_PROCESSED', 'Refund Processed'),
        ('CHARGEBACK', 'Chargeback'),
        ('DISPUTE', 'Dispute'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('FAILED', 'Failed'),
        ('IGNORED', 'Ignored'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    processor = models.CharField(max_length=50)  # stripe, paypal, etc.
    webhook_type = models.CharField(max_length=30, choices=WEBHOOK_TYPES)
    webhook_id = models.CharField(max_length=255)  # Processor's webhook ID
    
    # Event data
    event_data = models.JSONField()  # Full webhook payload
    signature = models.TextField(null=True, blank=True)  # Webhook signature for verification
    
    # Associated transaction
    payment_transaction = models.ForeignKey(
        PaymentTransaction, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='webhooks'
    )
    
    # Processing status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    processing_attempts = models.PositiveSmallIntegerField(default=0)
    last_attempt = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Metadata
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments_webhook'
        unique_together = ['processor', 'webhook_id']
        indexes = [
            models.Index(fields=['processor', 'webhook_type']),
            models.Index(fields=['status']),
            models.Index(fields=['received_at']),
            models.Index(fields=['payment_transaction']),
        ]
        ordering = ['-received_at']
    
    def __str__(self):
        return f"{self.processor} - {self.webhook_type} ({self.status})"

class PaymentRefund(models.Model):
    """Payment refund records"""
    REFUND_REASONS = [
        ('CUSTOMER_REQUEST', 'Customer Request'),
        ('MERCHANT_CANCEL', 'Merchant Cancellation'),
        ('FRAUD', 'Fraud Detection'),
        ('CHARGEBACK', 'Chargeback'),
        ('ERROR', 'Processing Error'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name='refunds')
    
    # Refund details
    refund_amount = models.DecimalField(max_digits=15, decimal_places=2)
    refund_currency = models.CharField(max_length=3)
    mtt_returned = models.DecimalField(max_digits=40, decimal_places=18, default=0)
    
    # Processing details
    processor_refund_id = models.CharField(max_length=255, null=True, blank=True)
    refund_reason = models.CharField(max_length=30, choices=REFUND_REASONS)
    reason_details = models.TextField(blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments_refund'
        indexes = [
            models.Index(fields=['original_transaction']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['initiated_by']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund for {self.original_transaction.reference_id} - {self.refund_amount} {self.refund_currency}"
