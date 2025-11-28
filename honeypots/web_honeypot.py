from flask import Flask, request, render_template_string, redirect
import requests
import json

app = Flask(__name__)

# HTML template for fake admin login
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel - Login</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; margin: 0; padding: 50px; }
        .login-box { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 3px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #007cba; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #005a87; }
        .error { color: red; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🔒 Admin Panel</h2>
        <form method="POST" action="/admin/login">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

def log_attack(client_ip, username, password, user_agent, path):
    """Send attack log to backend API"""
    try:
        data = {
            'source_ip': client_ip,
            'service': 'WEB',
            'username': username,
            'password': password,
            'request_data': f'Web login attempt at {path}',
            'user_agent': user_agent
        }
        
        response = requests.post('http://localhost:5000/api/logs', json=data, timeout=5)
        if response.status_code == 201:
            print(f"[LOG] Web attack logged: {client_ip} -> {username}:{password}")
        else:
            print(f"[ERROR] Failed to log attack: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Logging failed: {e}")

@app.route('/')
def index():
    return redirect('/admin')

@app.route('/admin')
def admin():
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    user_agent = request.headers.get('User-Agent', '')
    
    # Log the attack
    log_attack(client_ip, username, password, user_agent, '/admin/login')
    
    # Always show error (it's a honeypot!)
    return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials")

@app.route('/login')
def login():
    return redirect('/admin')

@app.route('/wp-admin')
def wp_admin():
    return redirect('/admin')

@app.route('/administrator')
def administrator():
    return redirect('/admin')

if __name__ == '__main__':
    print("[START] Web Honeypot running on http://0.0.0.0:8081")
    app.run(debug=False, host='0.0.0.0', port=8081)