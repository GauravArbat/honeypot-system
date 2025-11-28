import socket
import threading
import requests
import json
from datetime import datetime

class SSHHoneypot:
    def __init__(self, host='0.0.0.0', port=2222, api_url='http://localhost:5000/api/logs'):
        self.host = host
        self.port = port
        self.api_url = api_url
        self.banner = b"SSH-2.0-OpenSSH_7.4\r\n"
        
    def log_attack(self, client_ip, username, password):
        """Send attack log to backend API"""
        try:
            data = {
                'source_ip': client_ip,
                'service': 'SSH',
                'username': username,
                'password': password,
                'request_data': f'SSH login attempt: {username}:{password}',
                'user_agent': 'SSH Client'
            }
            
            response = requests.post(self.api_url, json=data, timeout=5)
            if response.status_code == 201:
                print(f"[LOG] Attack logged: {client_ip} -> {username}:{password}")
            else:
                print(f"[ERROR] Failed to log attack: {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Logging failed: {e}")
    
    def handle_client(self, client_socket, client_address):
        """Handle individual SSH connection"""
        client_ip = client_address[0]
        print(f"[CONNECT] New connection from {client_ip}")
        
        try:
            # Send SSH banner
            client_socket.send(self.banner)
            
            # Simple SSH protocol simulation
            client_socket.send(b"login: ")
            username = client_socket.recv(1024).decode().strip()
            
            client_socket.send(b"password: ")
            password = client_socket.recv(1024).decode().strip()
            
            # Log the attack
            self.log_attack(client_ip, username, password)
            
            # Send fake error and close
            client_socket.send(b"Access denied\r\n")
            
        except Exception as e:
            print(f"[ERROR] Client handling error: {e}")
        finally:
            client_socket.close()
            print(f"[DISCONNECT] Connection closed: {client_ip}")
    
    def start(self):
        """Start the SSH honeypot server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"[START] SSH Honeypot listening on {self.host}:{self.port}")
            
            while True:
                client_socket, client_address = server_socket.accept()
                
                # Handle each client in a separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n[STOP] SSH Honeypot stopped")
        except Exception as e:
            print(f"[ERROR] Server error: {e}")
        finally:
            server_socket.close()

if __name__ == "__main__":
    honeypot = SSHHoneypot()
    honeypot.start()