# DNS Validator Configuration
# Copy this file to config.py to customize settings

# DNS servers for propagation testing
# Format: (Name, IP Address)
DNS_SERVERS = [
    ("Google Primary", "8.8.8.8"),
    ("Google Secondary", "8.8.4.4"),
    ("Cloudflare Primary", "1.1.1.1"),
    ("Cloudflare Secondary", "1.0.0.1"),
    ("Quad9", "9.9.9.9"),
    ("OpenDNS", "208.67.222.222"),
    ("Verisign", "64.6.64.6"),
    ("Level3", "4.2.2.1"),
    # Add more servers as needed
    # ("Custom Server", "1.2.3.4"),
]

# Timeout settings (seconds)
DNS_TIMEOUT = 5
DNS_LIFETIME = 10

# Cloudflare API settings
CLOUDFLARE_API_BASE = "https://api.cloudflare.com/client/v4"

# Output settings
DEFAULT_TABLE_FORMAT = "grid"  # grid, simple, plain, html
MAX_CONCURRENT_QUERIES = 8

# Logging settings
LOG_FORMAT = "[{timestamp}] {level}: {message}"
TIMESTAMP_FORMAT = "%H:%M:%S"

# Color scheme (can be customized)
COLORS = {
    "SUCCESS": "green",
    "ERROR": "red", 
    "WARNING": "yellow",
    "INFO": "cyan",
    "HEADER": "magenta"
}