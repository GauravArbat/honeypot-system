# Honeypot System for Detecting Unauthorized Access and Attack Analysis

## Overview
A comprehensive honeypot system that detects unauthorized access attempts, logs attacker behavior, and provides real-time analytics through a web dashboard.

## Features
- **Multi-Service Honeypots**: SSH and Web login honeypots
- **Real-time Logging**: Captures IP, timestamps, credentials, and attack patterns
- **Analytics Dashboard**: Interactive charts and tables for attack visualization
- **Alert System**: Automated notifications for suspicious activities
- **IP Blocking**: Optional firewall integration for malicious IPs

## Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Honeypots     │───▶│   Backend API   │───▶│   Dashboard     │
│  (SSH/Web)      │    │   (Flask)       │    │   (React)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │    SQLite       │
                       │   (Logs DB)     │
                       └─────────────────┘
```

## Tech Stack
- **Backend**: Python Flask, SQLite
- **Frontend**: React, Chart.js
- **Honeypots**: Python (SSH), Flask (Web)
- **Database**: SQLite

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Run backend: `python backend/app.py`
3. Start honeypots: `python honeypots/ssh_honeypot.py`
4. Launch dashboard: `cd frontend && npm start`

## Security Note
⚠️ Run honeypots in isolated environment (VM/container) for security