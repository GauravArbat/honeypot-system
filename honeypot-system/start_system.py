#!/usr/bin/env python3
"""
Honeypot System Startup Script
Starts all components of the honeypot system
"""

import subprocess
import sys
import time
import os
from threading import Thread

def start_backend():
    """Start the Flask backend API"""
    print("Starting Backend API...")
    try:
        subprocess.run([sys.executable, "backend/app.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("Backend stopped")

def start_ssh_honeypot():
    """Start the SSH honeypot"""
    print("Starting SSH Honeypot...")
    try:
        subprocess.run([sys.executable, "honeypots/ssh_honeypot.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("SSH Honeypot stopped")

def start_web_honeypot():
    """Start the Web honeypot"""
    print("Starting Web Honeypot...")
    try:
        subprocess.run([sys.executable, "honeypots/web_honeypot.py"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("Web Honeypot stopped")

def start_frontend():
    """Start the React frontend"""
    print("Starting Frontend Dashboard...")
    try:
        subprocess.run(["npm", "start"], cwd="frontend")
    except KeyboardInterrupt:
        print("Frontend stopped")

def main():
    print("=" * 60)
    print("HONEYPOT SECURITY SYSTEM")
    print("=" * 60)
    print()
    
    # Check if SQLite is available (built into Python)
    print("Pre-flight checks...")
    try:
        import sqlite3
        print("SQLite database ready")
    except Exception as e:
        print(f"SQLite error: {e}")
        return
    
    print("All checks passed")
    print()
    
    # Start components in separate threads
    components = [
        ("Backend API", start_backend),
        ("SSH Honeypot", start_ssh_honeypot),
        ("Web Honeypot", start_web_honeypot),
    ]
    
    threads = []
    
    try:
        for name, func in components:
            thread = Thread(target=func, daemon=True)
            thread.start()
            threads.append(thread)
            time.sleep(2)  # Stagger startup
        
        print("All honeypot services started!")
        print()
        print("Access the dashboard at: http://localhost:3000")
        print("SSH Honeypot listening on: localhost:2222")
        print("Web Honeypot listening on: http://localhost:8080")
        print("API available at: http://localhost:5000")
        print()
        print("Press Ctrl+C to stop all services")
        
        # Start frontend (blocking)
        start_frontend()
        
    except KeyboardInterrupt:
        print("\nShutting down honeypot system...")
        print("All services stopped.")

if __name__ == "__main__":
    main()