# MTT Payment Gateway System

A comprehensive cryptocurrency payment gateway system built with Django for the MTT (MayTheToken) ecosystem. This system enables merchants to accept MTT token payments, provides trading functionality, marketplace integration, and comprehensive payment processing capabilities.

## System Architecture

The MTT Gateway consists of several interconnected modules based on the provided system diagram:

### Core Modules

1. **Tokens** - MTT token management, balances, transfers, and token operations
2. **Wallets** - Custodial and non-custodial wallet management with multi-signature support
3. **Merchants** - Merchant onboarding, gateway configuration, and business management
4. **Customers** - Customer profiles, KYC verification, and account management
5. **Payments** - Fiat-to-MTT conversion, payment processing, and transaction handling
6. **Canasale (Tech Provider)** - ERP integration, admin panels, and system configuration
7. **MayTheToken (Prop Trading Co.)** - Token issuer, routing engine, and trading operations
8. **WeedVader** - Marketplace functionality and card payment processing

## Features

### Payment Processing
- **Fiat-to-MTT Conversion**: Seamless conversion between fiat currencies and MTT tokens
- **Multiple Payment Methods**: Credit cards, bank transfers, digital wallets
- **Real-time Exchange Rates**: Dynamic pricing with multiple rate sources
- **Payment Routing**: Intelligent routing engine for optimal transaction paths

### Wallet Management
- **Multi-Wallet Support**: Custodial, non-custodial, and hybrid wallet types
- **Security Features**: Encrypted private keys, backup phrases, multi-signature support
- **Address Management**: Multiple addresses per wallet with derivation paths
- **Transaction History**: Comprehensive transaction tracking and analytics

### Merchant Features
- **Gateway Setup**: Quick and advanced setup options for payment gateways
- **Product Management**: Inventory tracking with MTT and fiat pricing
- **API Integration**: RESTful APIs with authentication and rate limiting
- **Settlement Options**: Automatic or manual settlement with configurable thresholds

### Trading & Liquidity
- **Order Management**: Market, limit, stop, and stop-limit orders
- **Liquidity Pools**: AMM-style liquidity provision with fee earning
- **Trading Pairs**: Multiple trading pairs with configurable fees
- **Routing Engine**: Multi-hop routing for optimal trade execution

### Marketplace
- **Product Listings**: Full marketplace functionality with categories
- **Order Processing**: Complete order lifecycle management
- **Fee Management**: Configurable commission rates and fee structures
- **Search & Discovery**: Advanced search with filtering and sorting

### Admin & Management
- **Admin Panels**: Customizable dashboards with role-based access
- **ERP Integration**: SAP, Oracle, QuickBooks, and custom ERP support
- **System Monitoring**: Real-time alerts and performance tracking
- **Configuration Management**: Global system settings and feature flags

## Technology Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Database**: PostgreSQL with optimized indexing
- **Caching**: Redis for session management and caching
- **Message Queue**: Celery with Redis broker
- **Real-time**: Django Channels for WebSocket connections
- **Blockchain**: Web3.py for Ethereum interaction
- **Payment Processing**: Stripe, PayPal integration
- **Security**: Advanced encryption, secure key management

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Node.js 16+ (for frontend, if applicable)

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd gateway
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database Setup**
```bash
# Create PostgreSQL database
createdb mtt_gateway_db

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Start Services**
```bash
# Start Redis (in separate terminal)
redis-server

# Start Celery worker (in separate terminal)
celery -A mtt_gateway worker -l info

# Start Django development server
python manage.py runserver
```

## Configuration

### Environment Variables

Key environment variables to configure:

```env
# Database
DB_NAME=mtt_gateway_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# MTT Token
MTT_CONTRACT_ADDRESS=0x...
MTT_CHAIN_ID=1
MTT_DECIMALS=18

# Blockchain
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
BLOCKCHAIN_PRIVATE_KEY=your_private_key

# Payment Processors
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLIC_KEY=pk_test_...

# Security
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### Initial Data Setup

1. **Create Token Configuration**
```bash
python manage.py shell
>>> from tokens.models import Token
>>> token = Token.objects.create(
...     name='MayTheToken',
...     symbol='MTT',
...     contract_address='0x...',
...     decimals=18
... )
```

2. **Configure Payment Methods**
```bash
>>> from payments.models import PaymentMethod
>>> PaymentMethod.objects.create(
...     name='Credit Card',
...     method_type='CREDIT_CARD',
...     is_active=True
... )
```

## API Documentation

### Authentication

The API uses token-based authentication. Obtain a token by posting to `/api/auth/token/` with valid credentials.

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -d "username=your_username&password=your_password"
```

### Key Endpoints

- **Tokens**: `/api/tokens/` - Token management and transfers
- **Wallets**: `/api/wallets/` - Wallet operations and management
- **Merchants**: `/api/merchant/` - Merchant account management
- **Payments**: `/api/payments/` - Payment processing and conversion
- **Trading**: `/api/maythetoken/` - Trading and routing operations
- **Marketplace**: `/api/weedvader/` - Marketplace functionality

### Example API Calls

**Create a payment transaction:**
```bash
curl -X POST http://localhost:8000/api/payments/transactions/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "fiat_amount": "100.00",
    "fiat_currency": "USD",
    "payment_method_id": "payment_method_uuid"
  }'
```

**Check wallet balance:**
```bash
curl -H "Authorization: Token your_token_here" \
  http://localhost:8000/api/wallets/balance/
```

## Database Schema

### Core Tables

- **tokens_token**: MTT token configuration
- **tokens_balance**: User token balances
- **tokens_transfer**: Token transfer records
- **wallets_wallet**: Wallet configurations
- **merchant_merchant**: Merchant accounts
- **payments_transaction**: Payment transactions
- **maythetoken_trading_pair**: Trading pairs
- **weedvader_marketplace**: Marketplace settings

### Relationships

The system uses UUID primary keys for security and scalability. Key relationships include:

- Users have multiple wallets and token balances
- Merchants have multiple gateways and products
- Customers have payment methods and transaction history
- Trading pairs have associated liquidity pools and orders

## Security Features

### Encryption
- Private keys encrypted with AES-256
- Database field-level encryption for sensitive data
- Secure backup phrase storage

### Access Control
- Role-based permissions (Super Admin, Admin, Manager, Operator)
- API rate limiting and authentication
- IP whitelisting for admin functions

### Monitoring
- Real-time transaction monitoring
- Suspicious activity detection
- Automated alert system

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
```bash
# Install development dependencies
pip install flake8 black isort

# Format code
black .
isort .

# Check code style
flake8 .
```

### Adding New Features

1. Create models in appropriate app
2. Add URL patterns and views
3. Create serializers for API endpoints
4. Add tests for new functionality
5. Update documentation

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure secure database credentials
- [ ] Set up SSL/TLS certificates
- [ ] Configure static file serving
- [ ] Set up monitoring and logging
- [ ] Configure backup procedures
- [ ] Set up load balancing (if needed)

### Docker Deployment

```bash
# Build Docker image
docker build -t mtt-gateway .

# Run with docker-compose
docker-compose up -d
```

## Monitoring & Maintenance

### Health Checks
- Database connectivity
- Redis connectivity
- Blockchain node status
- Payment processor availability

### Backup Procedures
- Daily database backups
- Encrypted wallet backup storage
- Configuration backup

### Performance Monitoring
- Transaction throughput
- API response times
- Database query performance
- Background job processing

## Support

### Getting Help

1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information
4. Contact the development team

### Common Issues

**Database Connection Errors**
- Verify PostgreSQL is running
- Check database credentials
- Ensure database exists

**Blockchain Connection Issues**
- Verify Ethereum RPC URL
- Check network connectivity
- Validate contract addresses

**Payment Processing Errors**
- Verify API keys for payment processors
- Check webhook configurations
- Review transaction logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Changelog

### Version 1.0.0 (Current)
- Initial implementation of all core modules
- Complete payment gateway functionality
- Trading and routing engine
- Marketplace integration
- Admin panel system
- ERP integration capabilities

---

For more detailed information about specific modules, refer to the individual app documentation in each module directory. 