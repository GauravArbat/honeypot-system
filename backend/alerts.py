import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sys
import os

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import *

class AlertManager:
    def __init__(self):
        self.email_enabled = EMAIL_ALERTS
        
    def send_email_alert(self, subject, message, ip_address, attack_count):
        """Send email alert for high-risk IP"""
        if not self.email_enabled:
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USERNAME
            msg['To'] = EMAIL_TO
            msg['Subject'] = f"🚨 Honeypot Alert: {subject}"
            
            body = f"""
HONEYPOT SECURITY ALERT

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Alert Type: High-Risk IP Detected
IP Address: {ip_address}
Attack Count: {attack_count}
Threshold: {ALERT_THRESHOLD}

Details:
{message}

This is an automated alert from your Honeypot Security System.
Please investigate this activity immediately.

Dashboard: http://localhost:3000
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_USERNAME, EMAIL_TO, text)
            server.quit()
            
            print(f"[ALERT] Email sent for IP {ip_address}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to send email alert: {e}")
            return False
    
    def console_alert(self, ip_address, attack_count, service):
        """Print console alert"""
        print("=" * 60)
        print("🚨 HIGH-RISK IP DETECTED 🚨")
        print("=" * 60)
        print(f"IP Address: {ip_address}")
        print(f"Attack Count: {attack_count}")
        print(f"Service: {service}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Threshold: {ALERT_THRESHOLD}")
        print("=" * 60)
    
    def check_and_alert(self, ip_address, attack_count, service="Unknown"):
        """Check if IP exceeds threshold and send alerts"""
        if attack_count >= ALERT_THRESHOLD:
            # Console alert
            self.console_alert(ip_address, attack_count, service)
            
            # Email alert
            if self.email_enabled:
                subject = f"High-Risk IP: {ip_address}"
                message = f"IP {ip_address} has made {attack_count} attack attempts on {service} service."
                self.send_email_alert(subject, message, ip_address, attack_count)
            
            return True
        return False

# Global alert manager instance
alert_manager = AlertManager()