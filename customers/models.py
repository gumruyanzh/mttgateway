from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

class CustomerProfile(models.Model):
    """Extended customer profile information"""
    VERIFICATION_LEVELS = [
        ('NONE', 'No Verification'),
        ('EMAIL', 'Email Verified'),
        ('PHONE', 'Phone Verified'),
        ('IDENTITY', 'Identity Verified'),
        ('FULL', 'Full KYC'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
        ('BANNED', 'Banned'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    
    # Personal information
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to='customer_avatars/', null=True, blank=True)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=2, blank=True)  # ISO country code
    
    # Verification status
    verification_level = models.CharField(max_length=20, choices=VERIFICATION_LEVELS, default='NONE')
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    identity_verified = models.BooleanField(default=False)
    
    # Account status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    is_premium = models.BooleanField(default=False)
    
    # Preferences
    preferred_currency = models.CharField(max_length=3, default='USD')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=True)
    
    # Security
    two_factor_enabled = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    referral_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='referrals'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'customers_profile'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['verification_level']),
            models.Index(fields=['status']),
            models.Index(fields=['referral_code']),
            models.Index(fields=['country']),
        ]
    
    def __str__(self):
        return f"{self.user.username} ({self.first_name} {self.last_name})"

class CustomerKYC(models.Model):
    """Customer KYC (Know Your Customer) information"""
    DOCUMENT_TYPES = [
        ('PASSPORT', 'Passport'),
        ('DRIVERS_LICENSE', 'Driver\'s License'),
        ('NATIONAL_ID', 'National ID'),
        ('UTILITY_BILL', 'Utility Bill'),
        ('BANK_STATEMENT', 'Bank Statement'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED', 'Expired'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='kyc_documents')
    
    # Document information
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=100, null=True, blank=True)
    document_file = models.FileField(upload_to='kyc_documents/', null=True, blank=True)
    document_front = models.ImageField(upload_to='kyc_documents/front/', null=True, blank=True)
    document_back = models.ImageField(upload_to='kyc_documents/back/', null=True, blank=True)
    selfie_photo = models.ImageField(upload_to='kyc_documents/selfies/', null=True, blank=True)
    
    # Verification details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_kyc_documents'
    )
    review_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Document validity
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    issuing_country = models.CharField(max_length=2, null=True, blank=True)  # ISO country code
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'customers_kyc'
        unique_together = ['customer', 'document_type']
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['document_type']),
        ]
    
    def __str__(self):
        return f"{self.customer.user.username} - {self.document_type} ({self.status})"

class CustomerActivity(models.Model):
    """Customer activity tracking"""
    ACTIVITY_TYPES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('PURCHASE', 'Purchase'),
        ('PAYMENT', 'Payment'),
        ('TRANSFER', 'Transfer'),
        ('WALLET_CREATE', 'Wallet Created'),
        ('KYC_SUBMIT', 'KYC Submitted'),
        ('PROFILE_UPDATE', 'Profile Updated'),
        ('PASSWORD_CHANGE', 'Password Changed'),
        ('API_ACCESS', 'API Access'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    
    # Request details
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_info = models.JSONField(default=dict, blank=True)
    location = models.JSONField(default=dict, blank=True)  # Geo location data
    
    # Associated data
    amount = models.DecimalField(
        max_digits=40, 
        decimal_places=18, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    currency = models.CharField(max_length=10, null=True, blank=True)
    transaction_id = models.UUIDField(null=True, blank=True)
    
    # Security flags
    is_suspicious = models.BooleanField(default=False)
    risk_score = models.PositiveSmallIntegerField(default=0)  # 0-100
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'customers_activity'
        indexes = [
            models.Index(fields=['customer', 'created_at']),
            models.Index(fields=['activity_type', 'created_at']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['is_suspicious']),
            models.Index(fields=['risk_score']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.user.username} - {self.activity_type}"

class CustomerSupport(models.Model):
    """Customer support tickets and communications"""
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('WAITING_CUSTOMER', 'Waiting for Customer'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('TECHNICAL', 'Technical Issue'),
        ('PAYMENT', 'Payment Issue'),
        ('ACCOUNT', 'Account Issue'),
        ('KYC', 'KYC/Verification'),
        ('SECURITY', 'Security Concern'),
        ('GENERAL', 'General Inquiry'),
        ('COMPLAINT', 'Complaint'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='support_tickets')
    
    # Ticket details
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    # Assignment
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tickets'
    )
    
    # Resolution
    resolution = models.TextField(blank=True)
    resolution_time = models.DurationField(null=True, blank=True)
    customer_rating = models.PositiveSmallIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    customer_feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'customers_support'
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['category']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['ticket_number']),
        ]
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Generate unique ticket number
            import random
            import string
            self.ticket_number = 'MTT-' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticket_number} - {self.subject}"

class CustomerNotification(models.Model):
    """Customer notifications and alerts"""
    NOTIFICATION_TYPES = [
        ('TRANSACTION', 'Transaction Alert'),
        ('SECURITY', 'Security Alert'),
        ('SYSTEM', 'System Notification'),
        ('MARKETING', 'Marketing'),
        ('SUPPORT', 'Support Update'),
        ('KYC', 'KYC Update'),
    ]
    
    CHANNELS = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push Notification'),
        ('IN_APP', 'In-App Notification'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('READ', 'Read'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='notifications')
    
    # Notification content
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    channel = models.CharField(max_length=20, choices=CHANNELS)
    
    # Delivery details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    is_urgent = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    action_url = models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers_notification'
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['channel']),
            models.Index(fields=['is_urgent']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.user.username} - {self.title}"
