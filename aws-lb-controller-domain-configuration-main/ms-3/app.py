from flask import Flask, render_template_string, jsonify
import datetime
import socket
import random

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App 3 - API Gateway</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .terminal {
            background: #1e1e1e;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from { transform: translateY(-30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .terminal-header {
            background: #2d2d2d;
            padding: 10px 20px;
            display: flex;
            gap: 10px;
        }
        
        .terminal-button {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        
        .terminal-button.red { background: #ff5f56; }
        .terminal-button.yellow { background: #ffbd2e; }
        .terminal-button.green { background: #27c93f; }
        
        .terminal-title {
            flex: 1;
            text-align: center;
            color: #fff;
            font-size: 0.9em;
        }
        
        .terminal-content {
            padding: 30px;
            color: #00ff00;
            font-family: 'Courier New', monospace;
        }
        
        .api-endpoint {
            background: #2d2d2d;
            margin: 15px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #00ff00;
            transition: all 0.3s;
        }
        
        .api-endpoint:hover {
            transform: translateX(10px);
            background: #3d3d3d;
        }
        
        .method {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .method.get { background: #4caf50; color: white; }
        .method.post { background: #2196f3; color: white; }
        .method.put { background: #ff9800; color: white; }
        .method.delete { background: #f44336; color: white; }
        
        .endpoint-url {
            color: #00ff00;
            font-family: monospace;
        }
        
        .response-example {
            background: #000;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            font-size: 0.8em;
            overflow-x: auto;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-box {
            background: #2d2d2d;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #00ff00;
        }
        
        .service-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            justify-content: center;
        }
        
        .service-btn {
            background: #2d2d2d;
            color: #00ff00;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.3s;
            border: 1px solid #00ff00;
        }
        
        .service-btn:hover {
            background: #00ff00;
            color: #000;
        }
        
        .blink {
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        .refresh-btn {
            background: #00ff00;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="terminal">
            <div class="terminal-header">
                <div class="terminal-button red"></div>
                <div class="terminal-button yellow"></div>
                <div class="terminal-button green"></div>
                <div class="terminal-title">api-gateway@eks:~/app3</div>
            </div>
            <div class="terminal-content">
                <div style="margin-bottom: 20px;">
                    <span class="blink">$</span> curl -X GET https://api.gateway.com/status
                    <div class="response-example">
                        {
                          "service": "APP-3 API Gateway",
                          "version": "3.0.0",
                          "status": "operational",
                          "uptime": "{{ uptime }}h"
                        }
                    </div>
                </div>
                
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-value">{{ total_requests }}</div>
                        <div>Total Requests</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{{ active_connections }}</div>
                        <div>Active Connections</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{{ avg_latency }}ms</div>
                        <div>Avg Latency</div>
                    </div>
                </div>
                
                <h3>📡 Available Endpoints:</h3>
                
                <div class="api-endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/app3</span>
                    <div class="response-example">
                        // Returns API Gateway dashboard (HTML)
                    </div>
                </div>
                
                <div class="api-endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/v1/data</span>
                    <div class="response-example">
                        {
                          "data": [...],
                          "metadata": {"total": 3, "version": "v1"}
                        }
                    </div>
                </div>
                
                <div class="api-endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/health</span>
                    <div class="response-example">
                        {"status": "healthy", "service": "app3"}
                    </div>
                </div>
                
                <div class="api-endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/</span>
                    <div class="response-example">
                        {"service": "APP-3 API Gateway", "status": "running"}
                    </div>
                </div>
                
                <div class="service-buttons">
                    <a href="/app1" class="service-btn">🎯 App 1</a>
                    <a href="/app2" class="service-btn">📊 App 2</a>
                    <a href="/app3" class="service-btn">🔌 App 3</a>
                </div>
                
                <div style="text-align: center; margin-top: 20px;">
                    <button class="refresh-btn" onclick="location.reload()">$ refresh --force</button>
                </div>
                
                <div style="margin-top: 20px; font-size: 0.8em; color: #666;">
                    Pod: {{ hostname }} | Last Updated: {{ timestamp }}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route("/app3")
def home():
    hostname = socket.gethostname()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_requests = random.randint(10000, 100000)
    active_connections = random.randint(50, 500)
    avg_latency = random.randint(10, 100)
    uptime = random.randint(100, 1000)
    
    return render_template_string(HTML_TEMPLATE,
                                  hostname=hostname,
                                  timestamp=timestamp,
                                  total_requests=total_requests,
                                  active_connections=active_connections,
                                  avg_latency=avg_latency,
                                  uptime=uptime)

@app.route("/")
def root():
    return {"service": "APP-3 API Gateway", "status": "running", "version": "3.0.0", "endpoints": ["/app3", "/api/v1/data", "/health"]}

@app.route("/health")
def health():
    return {"status": "healthy", "service": "app3"}

@app.route("/api/v1/data")
def get_data():
    return jsonify({
        "data": [
            {"id": 1, "name": "Customer Data", "value": random.randint(100, 1000)},
            {"id": 2, "name": "Analytics Metrics", "value": random.randint(100, 1000)},
            {"id": 3, "name": "API Calls", "value": random.randint(100, 1000)}
        ],
        "metadata": {
            "total": 3,
            "version": "v1",
            "timestamp": datetime.datetime.now().isoformat()
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
