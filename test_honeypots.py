#!/usr/bin/env python3
"""
Test script to simulate attacks on honeypots
Use this to generate test data for the dashboard
"""

import socket
import requests
import time
import random
from threading import Thread

# Test data
TEST_IPS = ['192.168.1.100', '10.0.0.50', '172.16.0.25', '203.0.113.10']
TEST_USERNAMES = ['admin', 'root', 'user', 'administrator', 'test', 'guest']
TEST_PASSWORDS = ['password', '123456', 'admin', 'root', 'password123', 'qwerty']

def test_ssh_honeypot():
    """Test SSH honeypot with fake login attempts"""
    print("🧪 Testing SSH Honeypot...")
    
    for i in range(5):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 2222))
            
            # Receive banner
            banner = sock.recv(1024)
            print(f"Received banner: {banner.decode().strip()}")
            
            # Send fake credentials
            username = random.choice(TEST_USERNAMES)
            password = random.choice(TEST_PASSWORDS)
            
            sock.recv(1024)  # "login: "
            sock.send(f"{username}\n".encode())
            
            sock.recv(1024)  # "password: "
            sock.send(f"{password}\n".encode())
            
            response = sock.recv(1024)
            print(f"Response: {response.decode().strip()}")
            
            sock.close()
            print(f"✅ SSH test {i+1}: {username}:{password}")
            
        except Exception as e:
            print(f"❌ SSH test {i+1} failed: {e}")
        
        time.sleep(1)

def test_web_honeypot():
    """Test Web honeypot with fake login attempts"""
    print("🧪 Testing Web Honeypot...")
    
    for i in range(5):
        try:
            username = random.choice(TEST_USERNAMES)
            password = random.choice(TEST_PASSWORDS)
            
            data = {
                'username': username,
                'password': password
            }
            
            response = requests.post('http://localhost:8080/admin/login', data=data)
            
            if response.status_code == 200:
                print(f"✅ Web test {i+1}: {username}:{password}")
            else:
                print(f"❌ Web test {i+1} failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Web test {i+1} failed: {e}")
        
        time.sleep(1)

def test_api():
    """Test API endpoints"""
    print("🧪 Testing API...")
    
    try:
        # Test stats endpoint
        response = requests.get('http://localhost:5000/api/stats')
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ API Stats: {stats['total_attacks']} total attacks")
        else:
            print(f"❌ API Stats failed: HTTP {response.status_code}")
        
        # Test attacks endpoint
        response = requests.get('http://localhost:5000/api/attacks?limit=5')
        if response.status_code == 200:
            attacks = response.json()
            print(f"✅ API Attacks: Retrieved {len(attacks['attacks'])} recent attacks")
        else:
            print(f"❌ API Attacks failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")

def main():
    print("=" * 50)
    print("🧪 HONEYPOT SYSTEM TESTING")
    print("=" * 50)
    print()
    
    print("Make sure all honeypot services are running first!")
    input("Press Enter to continue...")
    print()
    
    # Run tests
    test_ssh_honeypot()
    print()
    test_web_honeypot()
    print()
    test_api()
    print()
    
    print("🎉 Testing completed!")
    print("Check the dashboard at http://localhost:3000 to see the results")

if __name__ == "__main__":
    main()