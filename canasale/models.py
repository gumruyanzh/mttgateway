from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class SystemConfiguration(models.Model):
    """Global system configuration settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    data_type = models.CharField(
        max_length=20,
        choices=[
            ('STRING', 'String'),
            ('INTEGER', 'Integer'),
            ('DECIMAL', 'Decimal'),
            ('BOOLEAN', 'Boolean'),
            ('JSON', 'JSON'),
        ],
        default='STRING'
    )
    description = models.TextField(blank=True)
    is_encrypted = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)  # Can be accessed by frontend
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'canasale_config'
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f"{self.key}: {self.value[:50]}..."

class ERPIntegration(models.Model):
    """ERP system integration configurations"""
    INTEGRATION_TYPES = [
        ('SAP', 'SAP ERP'),
        ('ORACLE', 'Oracle ERP'),
        ('DYNAMICS', 'Microsoft Dynamics'),
        ('NETSUITE', 'NetSuite'),
        ('QUICKBOOKS', 'QuickBooks'),
        ('CUSTOM', 'Custom ERP'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ERROR', 'Error'),
        ('SYNCING', 'Syncing'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey('merchant.Merchant', on_delete=models.CASCADE, related_name='erp_integrations')
    
    # Integration details
    integration_type = models.CharField(max_length=20, choices=INTEGRATION_TYPES)
    name = models.CharField(max_length=100)
    api_endpoint = models.URLField()
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    
    # Configuration
    sync_interval_minutes = models.PositiveIntegerField(default=60)
    auto_sync = models.BooleanField(default=True)
    sync_orders = models.BooleanField(default=True)
    sync_customers = models.BooleanField(default=True)
    sync_products = models.BooleanField(default=True)
    sync_payments = models.BooleanField(default=True)
    
    # Status and monitoring
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INACTIVE')
    last_sync = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    sync_count = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'canasale_erp_integration'
        unique_together = ['merchant', 'name']
        indexes = [
            models.Index(fields=['merchant', 'status']),
            models.Index(fields=['integration_type']),
            models.Index(fields=['auto_sync', 'status']),
        ]
    
    def __str__(self):
        return f"{self.merchant.business_name} - {self.name} ({self.integration_type})"

class ERPSyncLog(models.Model):
    """ERP synchronization logs"""
    SYNC_TYPES = [
        ('ORDERS', 'Orders'),
        ('CUSTOMERS', 'Customers'),
        ('PRODUCTS', 'Products'),
        ('PAYMENTS', 'Payments'),
        ('INVENTORY', 'Inventory'),
    ]
    
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('PARTIAL', 'Partial Success'),
        ('FAILED', 'Failed'),
        ('SKIPPED', 'Skipped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    erp_integration = models.ForeignKey(ERPIntegration, on_delete=models.CASCADE, related_name='sync_logs')
    
    # Sync details
    sync_type = models.CharField(max_length=20, choices=SYNC_TYPES)
    records_processed = models.PositiveIntegerField(default=0)
    records_success = models.PositiveIntegerField(default=0)
    records_failed = models.PositiveIntegerField(default=0)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)
    sync_data = models.JSONField(default=dict, blank=True)  # Detailed sync information
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'canasale_erp_sync_log'
        indexes = [
            models.Index(fields=['erp_integration', 'started_at']),
            models.Index(fields=['sync_type', 'status']),
            models.Index(fields=['started_at']),
        ]
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.erp_integration.name} - {self.sync_type} ({self.status})"

class AdminPanel(models.Model):
    """Admin panel configurations and dashboards"""
    PANEL_TYPES = [
        ('DASHBOARD', 'Dashboard'),
        ('ANALYTICS', 'Analytics'),
        ('REPORTING', 'Reporting'),
        ('MONITORING', 'Monitoring'),
        ('CONFIGURATION', 'Configuration'),
    ]
    
    ACCESS_LEVELS = [
        ('SUPER_ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('OPERATOR', 'Operator'),
        ('READ_ONLY', 'Read Only'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    panel_type = models.CharField(max_length=20, choices=PANEL_TYPES)
    description = models.TextField(blank=True)
    
    # Access control
    required_access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS)
    allowed_users = models.ManyToManyField(User, blank=True, related_name='accessible_panels')
    allowed_groups = models.ManyToManyField('auth.Group', blank=True)
    
    # Configuration
    config_data = models.JSONField(default=dict, blank=True)  # Panel configuration
    layout_data = models.JSONField(default=dict, blank=True)  # Layout configuration
    
    # Status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_panels')
    
    class Meta:
        db_table = 'canasale_admin_panel'
        indexes = [
            models.Index(fields=['panel_type', 'is_active']),
            models.Index(fields=['required_access_level']),
            models.Index(fields=['sort_order']),
        ]
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.panel_type})"

class WebUIComponent(models.Model):
    """Web UI components and widgets"""
    COMPONENT_TYPES = [
        ('WIDGET', 'Widget'),
        ('CHART', 'Chart'),
        ('TABLE', 'Table'),
        ('FORM', 'Form'),
        ('BUTTON', 'Button'),
        ('MENU', 'Menu'),
        ('MODAL', 'Modal'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_panel = models.ForeignKey(AdminPanel, on_delete=models.CASCADE, related_name='components')
    
    # Component details
    name = models.CharField(max_length=100)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # Configuration
    config_data = models.JSONField(default=dict, blank=True)  # Component configuration
    data_source = models.CharField(max_length=100, blank=True)  # API endpoint or data source
    refresh_interval_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    # Layout
    position_x = models.PositiveSmallIntegerField(default=0)
    position_y = models.PositiveSmallIntegerField(default=0)
    width = models.PositiveSmallIntegerField(default=1)
    height = models.PositiveSmallIntegerField(default=1)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'canasale_web_ui_component'
        unique_together = ['admin_panel', 'name']
        indexes = [
            models.Index(fields=['admin_panel', 'is_active']),
            models.Index(fields=['component_type']),
            models.Index(fields=['position_x', 'position_y']),
        ]
    
    def __str__(self):
        return f"{self.admin_panel.name} - {self.name}"

class PaymentGatewaySetup(models.Model):
    """Non-custodial payment gateway setup configurations"""
    SETUP_TYPES = [
        ('QUICK_SETUP', 'Quick Setup'),
        ('ADVANCED_SETUP', 'Advanced Setup'),
        ('CUSTOM_SETUP', 'Custom Setup'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey('merchant.Merchant', on_delete=models.CASCADE, related_name='gateway_setups')
    
    # Setup details
    setup_type = models.CharField(max_length=20, choices=SETUP_TYPES)
    setup_config = models.JSONField(default=dict, blank=True)  # Setup configuration
    
    # Progress tracking
    current_step = models.PositiveSmallIntegerField(default=1)
    total_steps = models.PositiveSmallIntegerField(default=5)
    completed_steps = models.JSONField(default=list, blank=True)  # List of completed step numbers
    
    # Generated resources
    wallet_address = models.CharField(max_length=42, null=True, blank=True)
    api_key = models.CharField(max_length=64, null=True, blank=True)
    webhook_url = models.URLField(null=True, blank=True)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(blank=True)
    completion_percentage = models.PositiveSmallIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'canasale_gateway_setup'
        indexes = [
            models.Index(fields=['merchant', 'status']),
            models.Index(fields=['setup_type']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.merchant.business_name} - {self.setup_type} ({self.status})"

class SystemAlert(models.Model):
    """System alerts and notifications for administrators"""
    ALERT_TYPES = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    ALERT_CATEGORIES = [
        ('SYSTEM', 'System'),
        ('SECURITY', 'Security'),
        ('PAYMENT', 'Payment'),
        ('MAINTENANCE', 'Maintenance'),
        ('PERFORMANCE', 'Performance'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
        ('DISMISSED', 'Dismissed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Alert details
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    category = models.CharField(max_length=20, choices=ALERT_CATEGORIES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Metadata
    source_component = models.CharField(max_length=100, blank=True)  # Component that generated the alert
    related_object_id = models.UUIDField(null=True, blank=True)
    related_object_type = models.CharField(max_length=100, blank=True)
    
    # Status and assignment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_alerts'
    )
    acknowledged_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='acknowledged_alerts'
    )
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='resolved_alerts'
    )
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Auto-resolution
    auto_resolve_after_hours = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'canasale_system_alert'
        indexes = [
            models.Index(fields=['alert_type', 'status']),
            models.Index(fields=['category', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['assigned_to']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type}: {self.title}"
