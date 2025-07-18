# Generated by Django 4.2.7 on 2025-07-16 21:58

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('merchant', '0001_initial'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankProcessor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=200)),
                ('bank_code', models.CharField(max_length=20, unique=True)),
                ('bank_type', models.CharField(choices=[('COMMERCIAL', 'Commercial Bank'), ('INVESTMENT', 'Investment Bank'), ('CENTRAL', 'Central Bank'), ('CREDIT_UNION', 'Credit Union'), ('ONLINE', 'Online Bank')], max_length=20)),
                ('country', models.CharField(max_length=2)),
                ('api_endpoint', models.URLField(blank=True, null=True)),
                ('connection_type', models.CharField(choices=[('API', 'API Integration'), ('SFTP', 'SFTP'), ('MANUAL', 'Manual Processing')], default='API', max_length=20)),
                ('supports_instant_transfer', models.BooleanField(default=False)),
                ('supports_batch_transfer', models.BooleanField(default=True)),
                ('supports_international', models.BooleanField(default=False)),
                ('daily_limit', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('per_transaction_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('percentage_fee', models.DecimalField(decimal_places=4, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))])),
                ('domestic_processing_hours', models.PositiveIntegerField(default=24)),
                ('international_processing_hours', models.PositiveIntegerField(default=72)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('UNDER_REVIEW', 'Under Review'), ('SUSPENDED', 'Suspended')], default='INACTIVE', max_length=20)),
                ('is_primary', models.BooleanField(default=False)),
                ('total_transactions', models.PositiveIntegerField(default=0)),
                ('total_volume', models.DecimalField(decimal_places=2, default=0, max_digits=40)),
                ('success_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_used', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'weedvader_bank_processor',
            },
        ),
        migrations.CreateModel(
            name='Marketplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='marketplace_logos/')),
                ('commission_rate', models.DecimalField(decimal_places=4, default=Decimal('2.5'), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))])),
                ('min_listing_price', models.DecimalField(decimal_places=2, default=1, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('max_listing_price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('is_active', models.BooleanField(default=True)),
                ('requires_approval', models.BooleanField(default=True)),
                ('allow_external_sellers', models.BooleanField(default=True)),
                ('supported_currencies', models.JSONField(default=list)),
                ('default_currency', models.CharField(default='USD', max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'weedvader_marketplace',
            },
        ),
        migrations.CreateModel(
            name='MarketplaceListing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('subcategory', models.CharField(blank=True, max_length=100)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('model', models.CharField(blank=True, max_length=100)),
                ('condition', models.CharField(choices=[('NEW', 'New'), ('LIKE_NEW', 'Like New'), ('GOOD', 'Good'), ('FAIR', 'Fair'), ('POOR', 'Poor')], default='NEW', max_length=20)),
                ('price_usd', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('price_mtt', models.DecimalField(blank=True, decimal_places=18, max_digits=40, null=True, validators=[django.core.validators.MinValueValidator(Decimal('1E-18'))])),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('sku', models.CharField(blank=True, max_length=100)),
                ('primary_image', models.ImageField(blank=True, null=True, upload_to='marketplace_listings/')),
                ('additional_images', models.JSONField(blank=True, default=list)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING', 'Pending Approval'), ('ACTIVE', 'Active'), ('SOLD', 'Sold'), ('SUSPENDED', 'Suspended'), ('EXPIRED', 'Expired')], default='DRAFT', max_length=20)),
                ('is_featured', models.BooleanField(default=False)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('favorites_count', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('marketplace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='weedvader.marketplace')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketplace_listings', to='merchant.merchant')),
            ],
            options={
                'db_table': 'weedvader_marketplace_listing',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MarketplaceOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('unit_price_usd', models.DecimalField(decimal_places=2, max_digits=15)),
                ('unit_price_mtt', models.DecimalField(blank=True, decimal_places=18, max_digits=40, null=True)),
                ('total_amount_usd', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_amount_mtt', models.DecimalField(blank=True, decimal_places=18, max_digits=40, null=True)),
                ('marketplace_fee', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('payment_processing_fee', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('seller_net_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('shipping_address', models.JSONField(blank=True, default=dict)),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tracking_number', models.CharField(blank=True, max_length=100)),
                ('shipping_carrier', models.CharField(blank=True, max_length=50)),
                ('status', models.CharField(choices=[('PENDING', 'Pending Payment'), ('PAID', 'Paid'), ('PROCESSING', 'Processing'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled'), ('REFUNDED', 'Refunded'), ('DISPUTED', 'Disputed')], default='PENDING', max_length=20)),
                ('order_number', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shipped_at', models.DateTimeField(blank=True, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketplace_orders', to='customers.customerprofile')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weedvader.marketplacelisting')),
                ('marketplace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weedvader.marketplace')),
                ('payment_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.paymenttransaction')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketplace_sales', to='merchant.merchant')),
            ],
            options={
                'db_table': 'weedvader_marketplace_order',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FiatTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'Deposit'), ('WITHDRAWAL', 'Withdrawal'), ('TRANSFER', 'Transfer'), ('CONVERSION', 'Currency Conversion'), ('FEE_COLLECTION', 'Fee Collection')], max_length=20)),
                ('reference_number', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('currency', models.CharField(max_length=3)),
                ('from_account', models.CharField(blank=True, max_length=50, null=True)),
                ('to_account', models.CharField(blank=True, max_length=50, null=True)),
                ('from_account_name', models.CharField(blank=True, max_length=200, null=True)),
                ('to_account_name', models.CharField(blank=True, max_length=200, null=True)),
                ('transaction_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('exchange_rate', models.DecimalField(blank=True, decimal_places=8, max_digits=15, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed'), ('CANCELLED', 'Cancelled'), ('REVERSED', 'Reversed')], default='PENDING', max_length=20)),
                ('external_transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_confirmation_code', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('internal_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
                ('bank_processor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='weedvader.bankprocessor')),
                ('marketplace_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='weedvader.marketplaceorder')),
                ('payment_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.paymenttransaction')),
            ],
            options={
                'db_table': 'weedvader_fiat_transaction',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CardPaymentProcessor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('processor_type', models.CharField(choices=[('STRIPE', 'Stripe'), ('PAYPAL', 'PayPal'), ('SQUARE', 'Square'), ('ADYEN', 'Adyen'), ('AUTHORIZE_NET', 'Authorize.Net'), ('BRAINTREE', 'Braintree')], max_length=20)),
                ('api_endpoint', models.URLField()),
                ('api_key', models.CharField(max_length=255)),
                ('api_secret', models.CharField(max_length=255)),
                ('webhook_secret', models.CharField(blank=True, max_length=255, null=True)),
                ('supports_cards', models.BooleanField(default=True)),
                ('supports_digital_wallets', models.BooleanField(default=False)),
                ('supports_bank_transfers', models.BooleanField(default=False)),
                ('supports_subscriptions', models.BooleanField(default=False)),
                ('transaction_fee_percentage', models.DecimalField(decimal_places=4, default=Decimal('2.9'), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))])),
                ('fixed_fee_cents', models.PositiveIntegerField(default=30)),
                ('min_transaction_amount', models.DecimalField(decimal_places=2, default=1, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('max_transaction_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('TESTING', 'Testing'), ('MAINTENANCE', 'Maintenance')], default='INACTIVE', max_length=20)),
                ('is_default', models.BooleanField(default=False)),
                ('priority', models.PositiveSmallIntegerField(default=100)),
                ('success_rate', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))])),
                ('average_processing_time', models.DurationField(blank=True, null=True)),
                ('total_volume_processed', models.DecimalField(decimal_places=2, default=0, max_digits=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_used', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'weedvader_card_processor',
                'ordering': ['priority', '-success_rate'],
                'indexes': [models.Index(fields=['processor_type'], name='weedvader_c_process_4a010b_idx'), models.Index(fields=['status', 'priority'], name='weedvader_c_status_1fb2bf_idx'), models.Index(fields=['is_default'], name='weedvader_c_is_defa_eb2e34_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='bankprocessor',
            index=models.Index(fields=['bank_code'], name='weedvader_b_bank_co_648864_idx'),
        ),
        migrations.AddIndex(
            model_name='bankprocessor',
            index=models.Index(fields=['bank_type', 'country'], name='weedvader_b_bank_ty_8ae15f_idx'),
        ),
        migrations.AddIndex(
            model_name='bankprocessor',
            index=models.Index(fields=['status'], name='weedvader_b_status_25bbc4_idx'),
        ),
        migrations.AddIndex(
            model_name='bankprocessor',
            index=models.Index(fields=['is_primary'], name='weedvader_b_is_prim_632f39_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplaceorder',
            index=models.Index(fields=['buyer', 'status'], name='weedvader_m_buyer_i_8d925c_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplaceorder',
            index=models.Index(fields=['seller', 'status'], name='weedvader_m_seller__a315f9_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplaceorder',
            index=models.Index(fields=['marketplace', 'created_at'], name='weedvader_m_marketp_51541d_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplaceorder',
            index=models.Index(fields=['order_number'], name='weedvader_m_order_n_7aa266_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplaceorder',
            index=models.Index(fields=['status', 'created_at'], name='weedvader_m_status_ad0c15_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplacelisting',
            index=models.Index(fields=['marketplace', 'status'], name='weedvader_m_marketp_f027f8_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplacelisting',
            index=models.Index(fields=['seller', 'status'], name='weedvader_m_seller__67cb37_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplacelisting',
            index=models.Index(fields=['category', 'status'], name='weedvader_m_categor_441105_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplacelisting',
            index=models.Index(fields=['is_featured'], name='weedvader_m_is_feat_23a416_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplacelisting',
            index=models.Index(fields=['slug'], name='weedvader_m_slug_13da5a_idx'),
        ),
        migrations.AddIndex(
            model_name='marketplacelisting',
            index=models.Index(fields=['created_at'], name='weedvader_m_created_963013_idx'),
        ),
        migrations.AddIndex(
            model_name='fiattransaction',
            index=models.Index(fields=['bank_processor', 'status'], name='weedvader_f_bank_pr_01f395_idx'),
        ),
        migrations.AddIndex(
            model_name='fiattransaction',
            index=models.Index(fields=['reference_number'], name='weedvader_f_referen_5c1d59_idx'),
        ),
        migrations.AddIndex(
            model_name='fiattransaction',
            index=models.Index(fields=['transaction_type', 'created_at'], name='weedvader_f_transac_9c452f_idx'),
        ),
        migrations.AddIndex(
            model_name='fiattransaction',
            index=models.Index(fields=['status', 'created_at'], name='weedvader_f_status_3625d5_idx'),
        ),
        migrations.AddIndex(
            model_name='fiattransaction',
            index=models.Index(fields=['external_transaction_id'], name='weedvader_f_externa_c2a4d6_idx'),
        ),
    ]
