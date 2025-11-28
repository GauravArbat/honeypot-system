# Honeypot System Configuration

# Database Configuration
DATABASE_PATH = "honeypot.db"

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 5000
API_DEBUG = True

# Honeypot Configuration
SSH_HONEYPOT_HOST = "0.0.0.0"
SSH_HONEYPOT_PORT = 2222

WEB_HONEYPOT_HOST = "0.0.0.0"
WEB_HONEYPOT_PORT = 8080

# Alert Configuration
ALERT_THRESHOLD = 10  # Number of attempts before flagging as high-risk
EMAIL_ALERTS = False  # Set to True to enable email alerts
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587
EMAIL_USERNAME = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
EMAIL_TO = "admin@company.com"

# Security Configuration
RATE_LIMIT_ENABLED = True
MAX_REQUESTS_PER_MINUTE = 60

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "logs/honeypot.log"