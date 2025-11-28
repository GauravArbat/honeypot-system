# Honeypot System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Installation Guide](#installation-guide)
4. [Usage Instructions](#usage-instructions)
5. [API Documentation](#api-documentation)
6. [Security Considerations](#security-considerations)
7. [Troubleshooting](#troubleshooting)

## System Overview

### Purpose
The Honeypot System is designed to detect, log, and analyze unauthorized access attempts by simulating vulnerable services. It helps security teams understand attack patterns and improve their defensive strategies.

### Key Features
- **Multi-Protocol Support**: SSH and Web honeypots
- **Real-time Monitoring**: Live dashboard with attack statistics
- **Comprehensive Logging**: Detailed attack logs with IP, credentials, and timestamps
- **Visual Analytics**: Charts and graphs for attack pattern analysis
- **Alert System**: Configurable thresholds for high-risk IP detection

## Architecture

### Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Honeypots     │───▶│   Backend API   │───▶│   Dashboard     │
│                 │    │                 │    │                 │
│ • SSH (Port 2222)│    │ • Flask Server  │    │ • React App     │
│ • Web (Port 8080)│    │ • MongoDB       │    │ • Charts        │
│                 │    │ • Analytics     │    │ • Tables        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow
1. **Attack Detection**: Honeypots capture connection attempts
2. **Data Logging**: Attack details sent to backend API
3. **Storage**: MongoDB stores structured attack logs
4. **Analytics**: Backend processes data for statistics
5. **Visualization**: Dashboard displays real-time insights

## Installation Guide

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB 4.4+
- Git

### Step 1: Clone and Setup
```bash
cd c:\Users\Gaurav Arbat\Desktop\cis\honeypot-system
pip install -r requirements.txt
```

### Step 2: Database Setup
```bash
# Start MongoDB service
net start MongoDB

# Create database (automatic on first use)
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
```

### Step 4: Configuration
Edit `config/config.py` to customize:
- Database connection
- Port numbers
- Alert thresholds
- Email settings

## Usage Instructions

### Starting the System

#### Option 1: All-in-One Startup
```bash
python start_system.py
```

#### Option 2: Manual Startup
```bash
# Terminal 1: Backend API
python backend/app.py

# Terminal 2: SSH Honeypot
python honeypots/ssh_honeypot.py

# Terminal 3: Web Honeypot
python honeypots/web_honeypot.py

# Terminal 4: Frontend Dashboard
cd frontend && npm start
```

### Accessing Services
- **Dashboard**: http://localhost:3000
- **Web Honeypot**: http://localhost:8080
- **SSH Honeypot**: localhost:2222
- **API**: http://localhost:5000

### Testing the System
```bash
python test_honeypots.py
```

## API Documentation

### Endpoints

#### POST /api/logs
Add new attack log entry
```json
{
  "source_ip": "192.168.1.100",
  "service": "SSH",
  "username": "admin",
  "password": "password123",
  "request_data": "SSH login attempt",
  "user_agent": "SSH Client"
}
```

#### GET /api/stats
Get attack statistics
```json
{
  "total_attacks": 150,
  "attacks_today": 25,
  "unique_ips": 45,
  "top_ips": [...],
  "top_usernames": [...]
}
```

#### GET /api/attacks
Get paginated attack logs
- Parameters: `page`, `limit`
- Returns: Attack list with pagination info

#### GET /api/attacks/timeline
Get attack timeline data
- Parameters: `days` (default: 7)
- Returns: Daily attack counts

#### GET /api/alerts
Get high-risk IPs
- Parameters: `threshold` (default: 10)
- Returns: IPs exceeding threshold

## Security Considerations

### Isolation Requirements
⚠️ **CRITICAL**: Run honeypots in isolated environment

#### Recommended Setup
1. **Virtual Machine**: Dedicated VM for honeypots
2. **Network Segmentation**: Separate VLAN/subnet
3. **Firewall Rules**: Restrict honeypot network access
4. **Monitoring**: Log all honeypot network traffic

### Security Best Practices
- Never run on production networks
- Use non-standard ports when possible
- Regular security updates
- Monitor honeypot integrity
- Backup attack logs regularly

### Data Protection
- Encrypt stored credentials
- Anonymize IP addresses if required
- Comply with data retention policies
- Secure API endpoints

## Troubleshooting

### Common Issues

#### MongoDB Connection Failed
```
Error: ServerSelectionTimeoutError
```
**Solution**: 
- Ensure MongoDB service is running
- Check connection string in config
- Verify firewall settings

#### Port Already in Use
```
Error: [Errno 98] Address already in use
```
**Solution**:
- Change port in configuration
- Kill existing processes: `netstat -tulpn | grep :2222`

#### Frontend Build Errors
```
Error: Module not found
```
**Solution**:
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check Node.js version compatibility

#### No Attack Data Showing
**Checklist**:
- Backend API running and accessible
- MongoDB service active
- Honeypots successfully logging to API
- Check browser console for errors

### Log Files
- Backend logs: Console output
- Honeypot logs: Console output
- MongoDB logs: `/var/log/mongodb/mongod.log`

### Performance Tuning
- Increase MongoDB connection pool
- Add database indexes for queries
- Implement log rotation
- Monitor system resources

## Advanced Configuration

### Email Alerts
```python
# config/config.py
EMAIL_ALERTS = True
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_USERNAME = "alerts@company.com"
EMAIL_PASSWORD = "app-password"
```

### Custom Honeypot Services
Extend the system by creating new honeypot modules:
1. Create new Python script in `honeypots/`
2. Implement logging to API
3. Add service type to dashboard
4. Update documentation

### Database Optimization
```javascript
// MongoDB indexes for better performance
db.attack_logs.createIndex({"timestamp": -1})
db.attack_logs.createIndex({"source_ip": 1})
db.attack_logs.createIndex({"service": 1})
```

## Project Structure
```
honeypot-system/
├── backend/
│   └── app.py              # Flask API server
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main dashboard component
│   │   └── App.css         # Dashboard styles
│   └── package.json        # Frontend dependencies
├── honeypots/
│   ├── ssh_honeypot.py     # SSH honeypot service
│   └── web_honeypot.py     # Web honeypot service
├── config/
│   └── config.py           # System configuration
├── requirements.txt        # Python dependencies
├── start_system.py         # Startup script
├── test_honeypots.py       # Testing script
└── README.md              # Project overview
```