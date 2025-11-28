from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import sqlite3
import json
import os

app = Flask(__name__)
CORS(app)

# SQLite database setup
DB_PATH = 'honeypot.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS attack_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source_ip TEXT NOT NULL,
            service TEXT NOT NULL,
            username TEXT,
            password TEXT,
            request_data TEXT,
            user_agent TEXT,
            country TEXT DEFAULT 'Unknown'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/logs', methods=['POST'])
def add_log():
    """Add new attack log entry"""
    try:
        data = request.json
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            INSERT INTO attack_logs (timestamp, source_ip, service, username, password, request_data, user_agent, country)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.utcnow().isoformat(),
            data.get('source_ip'),
            data.get('service'),
            data.get('username'),
            data.get('password'),
            data.get('request_data', ''),
            data.get('user_agent', ''),
            data.get('country', 'Unknown')
        ))
        conn.commit()
        log_id = conn.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': log_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get attack statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Total attacks
        total_attacks = conn.execute('SELECT COUNT(*) FROM attack_logs').fetchone()[0]
        
        # Attacks today
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        attacks_today = conn.execute('SELECT COUNT(*) FROM attack_logs WHERE timestamp >= ?', (today,)).fetchone()[0]
        
        # Unique IPs
        unique_ips = conn.execute('SELECT COUNT(DISTINCT source_ip) FROM attack_logs').fetchone()[0]
        
        # Top attacking IPs
        top_ips = conn.execute('''
            SELECT source_ip as _id, COUNT(*) as count 
            FROM attack_logs 
            GROUP BY source_ip 
            ORDER BY count DESC 
            LIMIT 10
        ''').fetchall()
        top_ips = [{'_id': row[0], 'count': row[1]} for row in top_ips]
        
        # Top usernames
        top_usernames = conn.execute('''
            SELECT username as _id, COUNT(*) as count 
            FROM attack_logs 
            WHERE username IS NOT NULL 
            GROUP BY username 
            ORDER BY count DESC 
            LIMIT 10
        ''').fetchall()
        top_usernames = [{'_id': row[0], 'count': row[1]} for row in top_usernames]
        
        conn.close()
        
        return jsonify({
            'total_attacks': total_attacks,
            'attacks_today': attacks_today,
            'unique_ips': unique_ips,
            'top_ips': top_ips,
            'top_usernames': top_usernames
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attacks/timeline', methods=['GET'])
def get_timeline():
    """Get attacks timeline for charts"""
    try:
        days = int(request.args.get('days', 7))
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        
        conn = sqlite3.connect(DB_PATH)
        timeline = conn.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM attack_logs 
            WHERE timestamp >= ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (start_date,)).fetchall()
        
        # Format for frontend
        result = []
        for row in timeline:
            date_parts = row[0].split('-')
            result.append({
                '_id': {'day': int(date_parts[2]), 'month': int(date_parts[1]), 'year': int(date_parts[0])},
                'count': row[1]
            })
        
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attacks', methods=['GET'])
def get_attacks():
    """Get paginated attack logs"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        offset = (page - 1) * limit
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        
        attacks = conn.execute('''
            SELECT * FROM attack_logs 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset)).fetchall()
        
        attacks = [dict(row) for row in attacks]
        
        total = conn.execute('SELECT COUNT(*) FROM attack_logs').fetchone()[0]
        conn.close()
        
        return jsonify({
            'attacks': attacks,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get high-risk IPs (multiple attempts)"""
    try:
        threshold = int(request.args.get('threshold', 10))
        
        conn = sqlite3.connect(DB_PATH)
        alerts = conn.execute('''
            SELECT source_ip as _id, COUNT(*) as count
            FROM attack_logs 
            GROUP BY source_ip 
            HAVING count >= ?
            ORDER BY count DESC
        ''', (threshold,)).fetchall()
        
        alerts = [{'_id': row[0], 'count': row[1]} for row in alerts]
        conn.close()
        
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)