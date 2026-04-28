from flask import Flask, render_template_string
import datetime
import socket
import random

app = Flask(__name__)

# HTML template for the main page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App 1 - Customer Service Portal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Animated background bubbles */
        .bubble {
            position: absolute;
            bottom: -100px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            animation: rise 20s infinite ease-in;
            z-index: 0;
        }
        
        @keyframes rise {
            0% {
                bottom: -100px;
                transform: translateX(0);
            }
            50% {
                transform: translateX(100px);
            }
            100% {
                bottom: 1080px;
                transform: translateX(-200px);
            }
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            max-width: 900px;
            width: 100%;
            animation: slideIn 0.6s ease-out;
            position: relative;
            z-index: 1;
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 10s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translate(-30%, -30%) rotate(0deg); }
            100% { transform: translate(30%, 30%) rotate(360deg); }
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            position: relative;
        }
        
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
            position: relative;
        }
        
        .status {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #4caf50;
            animation: pulse 2s infinite;
            margin-right: 5px;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }
        
        .content {
            padding: 40px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        @keyframes fadeInUp {
            from {
                transform: translateY(20px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            margin-top: 10px;
        }
        
        .info-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }
        
        .info-card:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .info-item:last-child {
            border-bottom: none;
        }
        
        .info-label {
            font-weight: bold;
            color: #555;
        }
        
        .info-value {
            color: #333;
            font-family: monospace;
        }
        
        .service-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .service-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .service-card:hover {
            border-color: #667eea;
            transform: scale(1.05);
        }
        
        .service-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        .refresh-btn {
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 10px;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
        }
        
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102,126,234,0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Customer Service Portal</h1>
            <p>Microservices Demo - Application 1</p>
            <div class="badge">
                <span class="status"></span> System Operational
            </div>
        </div>
        
        <div class="content">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ active_customers }}</div>
                    <div class="stat-label">Active Customers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ tickets_today }}</div>
                    <div class="stat-label">Tickets Today</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ satisfaction_rate }}%</div>
                    <div class="stat-label">Satisfaction Rate</div>
                </div>
            </div>
            
            <div class="info-card">
                <h3>📊 Service Information</h3>
                <div class="info-item">
                    <span class="info-label">Application Name:</span>
                    <span class="info-value">APP-1 Customer Service</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Version:</span>
                    <span class="info-value">3.0.0</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Pod Hostname:</span>
                    <span class="info-value">{{ hostname }}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Current Time:</span>
                    <span class="info-value">{{ timestamp }}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Response Time:</span>
                    <span class="info-value">{{ response_time }}ms</span>
                </div>
            </div>
            
            <div class="info-card">
                <h3>🔗 Microservices Ecosystem</h3>
                <div class="service-grid">
                    <div class="service-card" onclick="window.location.href='/app1'">
                        <div class="service-icon">🎯</div>
                        <div><strong>App 1</strong></div>
                        <div style="font-size: 0.8em; color: #667eea;">Customer Service</div>
                    </div>
                    <div class="service-card" onclick="window.location.href='/app2'">
                        <div class="service-icon">📊</div>
                        <div><strong>App 2</strong></div>
                        <div style="font-size: 0.8em; color: #f5576c;">Analytics</div>
                    </div>
                    <div class="service-card" onclick="window.location.href='/app3'">
                        <div class="service-icon">🔌</div>
                        <div><strong>App 3</strong></div>
                        <div style="font-size: 0.8em; color: #4facfe;">API Gateway</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Powered by Flask | Kubernetes | AWS EKS</p>
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        </div>
    </div>
    
    <script>
        // Create animated bubbles
        for(let i = 0; i < 20; i++) {
            let bubble = document.createElement('div');
            bubble.className = 'bubble';
            bubble.style.width = Math.random() * 100 + 50 + 'px';
            bubble.style.height = bubble.style.width;
            bubble.style.left = Math.random() * 100 + '%';
            bubble.style.animationDelay = Math.random() * 20 + 's';
            bubble.style.animationDuration = Math.random() * 15 + 10 + 's';
            document.body.appendChild(bubble);
        }
    </script>
</body>
</html>
'''

@app.route("/app1")
def home():
    hostname = socket.gethostname()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    active_customers = random.randint(1000, 5000)
    tickets_today = random.randint(50, 200)
    satisfaction_rate = random.randint(85, 99)
    response_time = random.randint(10, 50)
    
    return render_template_string(HTML_TEMPLATE, 
                                  hostname=hostname,
                                  timestamp=timestamp,
                                  active_customers=active_customers,
                                  tickets_today=tickets_today,
                                  satisfaction_rate=satisfaction_rate,
                                  response_time=response_time)

@app.route("/")
def root():
    return {"service": "APP-1 Customer Service", "status": "running", "version": "3.0.0"}

@app.route("/health")
def health():
    return {"status": "healthy", "service": "app1"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
