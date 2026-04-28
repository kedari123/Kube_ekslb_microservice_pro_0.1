from flask import Flask, render_template_string
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
    <title>App 2 - Analytics Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            animation: fadeIn 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #f5576c;
            margin-bottom: 10px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: transform 0.3s;
            animation: slideUp 0.5s ease-out;
        }
        
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-label {
            color: #666;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
        }
        
        .chart-title {
            font-size: 1.2em;
            margin-bottom: 20px;
            color: #333;
        }
        
        .bar-chart {
            display: flex;
            align-items: flex-end;
            gap: 20px;
            height: 200px;
            margin-top: 20px;
        }
        
        .bar {
            flex: 1;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 5px;
            transition: height 1s ease;
            animation: growBar 1s ease-out;
        }
        
        @keyframes growBar {
            from { height: 0; }
            to { height: var(--height); }
        }
        
        .bar-label {
            text-align: center;
            margin-top: 10px;
            font-size: 0.8em;
            color: #666;
        }
        
        .service-links {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 20px;
        }
        
        .service-btn {
            padding: 10px 20px;
            background: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            color: #333;
            display: inline-block;
        }
        
        .service-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .refresh-btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(245,87,108,0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Real-Time Analytics Dashboard</h1>
            <p>Application 2 - Live Metrics & Monitoring</p>
            <div class="badge">Last Updated: {{ timestamp }}</div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{{ cpu_usage }}%</div>
                <div class="metric-label">CPU Usage</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ memory_usage }}MB</div>
                <div class="metric-label">Memory Usage</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ requests_per_sec }}</div>
                <div class="metric-label">Requests/Second</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ avg_response }}ms</div>
                <div class="metric-label">Avg Response Time</div>
            </div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">📊 Request Volume (Last 5 minutes)</div>
            <div class="bar-chart">
                <div style="flex: 1;">
                    <div class="bar" style="height: {{ bar1 }}px; --height: {{ bar1 }}px"></div>
                    <div class="bar-label">Min 1</div>
                </div>
                <div style="flex: 1;">
                    <div class="bar" style="height: {{ bar2 }}px; --height: {{ bar2 }}px"></div>
                    <div class="bar-label">Min 2</div>
                </div>
                <div style="flex: 1;">
                    <div class="bar" style="height: {{ bar3 }}px; --height: {{ bar3 }}px"></div>
                    <div class="bar-label">Min 3</div>
                </div>
                <div style="flex: 1;">
                    <div class="bar" style="height: {{ bar4 }}px; --height: {{ bar4 }}px"></div>
                    <div class="bar-label">Min 4</div>
                </div>
                <div style="flex: 1;">
                    <div class="bar" style="height: {{ bar5 }}px; --height: {{ bar5 }}px"></div>
                    <div class="bar-label">Min 5</div>
                </div>
            </div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">🖥️ System Information</div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0;">
                <span>Pod Hostname:</span>
                <strong>{{ hostname }}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0;">
                <span>Active Sessions:</span>
                <strong>{{ active_sessions }}</strong>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0;">
                <span>Uptime:</span>
                <strong>{{ uptime }} hours</strong>
            </div>
        </div>
        
        <div class="service-links">
            <a href="/app1" class="service-btn">🎯 App 1 - Customer Service</a>
            <a href="/app2" class="service-btn">📊 App 2 - Analytics</a>
            <a href="/app3" class="service-btn">🔌 App 3 - API Gateway</a>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Metrics</button>
        </div>
    </div>
</body>
</html>
'''

@app.route("/app2")
def home():
    hostname = socket.gethostname()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate realistic metrics
    cpu_usage = random.randint(10, 80)
    memory_usage = random.randint(128, 512)
    requests_per_sec = random.randint(50, 300)
    avg_response = random.randint(10, 100)
    active_sessions = random.randint(100, 1000)
    uptime = random.randint(100, 1000)
    
    # Bar chart data
    bar1 = random.randint(50, 200)
    bar2 = random.randint(50, 200)
    bar3 = random.randint(50, 200)
    bar4 = random.randint(50, 200)
    bar5 = random.randint(50, 200)
    
    return render_template_string(HTML_TEMPLATE,
                                  hostname=hostname,
                                  timestamp=timestamp,
                                  cpu_usage=cpu_usage,
                                  memory_usage=memory_usage,
                                  requests_per_sec=requests_per_sec,
                                  avg_response=avg_response,
                                  active_sessions=active_sessions,
                                  uptime=uptime,
                                  bar1=bar1, bar2=bar2, bar3=bar3, bar4=bar4, bar5=bar5)

@app.route("/")
def root():
    return {"service": "APP-2 Analytics Dashboard", "status": "running", "version": "3.0.0"}

@app.route("/health")
def health():
    return {"status": "healthy", "service": "app2"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
