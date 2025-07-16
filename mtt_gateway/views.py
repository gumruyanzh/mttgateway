from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    """
    MTT Payment Gateway Homepage
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MTT Payment Gateway</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
            }
            .header {
                text-align: center;
                margin-bottom: 50px;
            }
            .header h1 {
                font-size: 3em;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                font-size: 1.2em;
                margin: 10px 0 0 0;
                opacity: 0.9;
            }
            .modules-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }
            .module-card {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 25px;
                border: 1px solid rgba(255,255,255,0.2);
                transition: transform 0.3s ease;
            }
            .module-card:hover {
                transform: translateY(-5px);
            }
            .module-card h3 {
                margin: 0 0 15px 0;
                color: #fff;
                font-size: 1.3em;
            }
            .module-card p {
                margin: 0 0 15px 0;
                opacity: 0.9;
                line-height: 1.5;
            }
            .module-card a {
                color: #fff;
                text-decoration: none;
                font-weight: 500;
                border: 1px solid rgba(255,255,255,0.3);
                padding: 8px 16px;
                border-radius: 5px;
                display: inline-block;
                transition: all 0.3s ease;
            }
            .module-card a:hover {
                background: rgba(255,255,255,0.2);
                border-color: rgba(255,255,255,0.5);
            }
            .admin-section {
                text-align: center;
                margin-top: 40px;
                padding: 30px;
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                border: 1px solid rgba(255,255,255,0.2);
            }
            .admin-btn {
                background: #4CAF50;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                display: inline-block;
                margin: 10px;
                transition: background 0.3s ease;
            }
            .admin-btn:hover {
                background: #45a049;
            }
            .status {
                text-align: center;
                margin: 20px 0;
                padding: 15px;
                background: rgba(76, 175, 80, 0.2);
                border-radius: 8px;
                border: 1px solid rgba(76, 175, 80, 0.3);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 MTT Payment Gateway</h1>
                <p>Multi-Token Trading & Payment Processing Platform</p>
            </div>
            
            <div class="status">
                <strong>✅ System Status: Online</strong><br>
                All modules are loaded and ready for use
            </div>

            <div class="modules-grid">
                <div class="module-card">
                    <h3>🪙 Tokens</h3>
                    <p>MTT token management, balances, transfers, and pricing system</p>
                    <a href="/api/tokens/">Access API</a>
                </div>
                
                <div class="module-card">
                    <h3>👛 Wallets</h3>
                    <p>Custodial and non-custodial wallet management with security features</p>
                    <a href="/api/wallets/">Access API</a>
                </div>
                
                <div class="module-card">
                    <h3>🏪 Merchants</h3>
                    <p>Business accounts, payment gateways, and product management</p>
                    <a href="/api/merchant/">Access API</a>
                </div>
                
                <div class="module-card">
                    <h3>👥 Customers</h3>
                    <p>User profiles, KYC verification, and activity tracking</p>
                    <a href="/api/customers/">Access API</a>
                </div>
                
                <div class="module-card">
                    <h3>💳 Payments</h3>
                    <p>Fiat-to-MTT conversion and payment processing system</p>
                    <a href="/api/payments/">Access API</a>
                </div>
                
                <div class="module-card">
                    <h3>📈 MayTheToken</h3>
                    <p>Token trading, routing engine, and liquidity management</p>
                    <a href="/api/maythetoken/">Access API</a>
                </div>
                
                <div class="module-card">
                    <h3>⚙️ Canasale</h3>
                    <p>ERP integration, admin panels, and system configuration</p>
                    <a href="/api/canasale/">Access API</a>
                </div>
                
                <div class="module-card">
                    <h3>🛒 WeedVader</h3>
                    <p>Marketplace functionality and card payment processing</p>
                    <a href="/api/weedvader/">Access API</a>
                </div>
            </div>

            <div class="admin-section">
                <h3>🔧 Administration</h3>
                <p>Manage your MTT Gateway system</p>
                <a href="/admin/" class="admin-btn">Django Admin Panel</a>
                <br><br>
                <small>Login: admin / admin123</small>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content.encode('utf-8'), content_type='text/html') 