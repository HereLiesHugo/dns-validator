"""
DNS Validator - Utility Functions

Common utility functions used across the DNS validator modules.

Author: Matisse Urquhart
License: GNU AGPL v3.0
"""

import socket
import ipaddress
import requests
from typing import List, Dict, Optional, Tuple
from colorama import Fore, Style


def is_valid_domain(domain: str) -> bool:
    """
    Validate if a string is a valid domain name.
    
    Args:
        domain: Domain name to validate
        
    Returns:
        bool: True if valid domain, False otherwise
    """
    if not domain or len(domain) > 253:
        return False
        
    # Remove trailing dot if present
    if domain.endswith('.'):
        domain = domain[:-1]
        
    # Check each label
    labels = domain.split('.')
    if len(labels) < 2:
        return False
        
    for label in labels:
        if not label or len(label) > 63:
            return False
        if not label.replace('-', '').replace('_', '').isalnum():
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
            
    return True


def is_valid_ip(ip: str) -> bool:
    """
    Check if a string is a valid IP address (IPv4 or IPv6).
    
    Args:
        ip: IP address to validate
        
    Returns:
        bool: True if valid IP, False otherwise
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_ipv4(ip: str) -> bool:
    """
    Check if an IP address is IPv4.
    
    Args:
        ip: IP address to check
        
    Returns:
        bool: True if IPv4, False otherwise
    """
    try:
        return isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address)
    except ValueError:
        return False


def is_ipv6(ip: str) -> bool:
    """
    Check if an IP address is IPv6.
    
    Args:
        ip: IP address to check
        
    Returns:
        bool: True if IPv6, False otherwise
    """
    try:
        return isinstance(ipaddress.ip_address(ip), ipaddress.IPv6Address)
    except ValueError:
        return False


def reverse_dns_lookup(ip: str) -> Optional[str]:
    """
    Perform reverse DNS lookup for an IP address.
    
    Args:
        ip: IP address to lookup
        
    Returns:
        str or None: Hostname if found, None if lookup fails
    """
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except (socket.herror, socket.gaierror, OSError):
        return None


def get_ip_geolocation(ip: str) -> Dict:
    """
    Get geolocation information for an IP address using ipapi.co.
    
    Args:
        ip: IP address to lookup
        
    Returns:
        dict: Geolocation data or empty dict if lookup fails
    """
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    return {}


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration string
    """
    if seconds < 1:
        return f"{seconds*1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def format_bytes(bytes_val: int) -> str:
    """
    Format bytes to human-readable string.
    
    Args:
        bytes_val: Number of bytes
        
    Returns:
        str: Formatted bytes string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"


def colorize_status(status: str, message: str) -> str:
    """
    Colorize status messages based on status type.
    
    Args:
        status: Status type (success, warning, error, info)
        message: Message to colorize
        
    Returns:
        str: Colorized message
    """
    colors = {
        'success': Fore.GREEN,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'info': Fore.CYAN,
        'debug': Fore.MAGENTA
    }
    
    color = colors.get(status.lower(), Fore.WHITE)
    return f"{color}{message}{Style.RESET_ALL}"


def clean_domain_list(domains: List[str]) -> List[str]:
    """
    Clean and validate a list of domain names.
    
    Args:
        domains: List of domain names to clean
        
    Returns:
        list: List of clean, valid domain names
    """
    cleaned = []
    for domain in domains:
        if isinstance(domain, str):
            domain = domain.strip().lower()
            # Remove protocol prefixes
            if domain.startswith(('http://', 'https://')):
                domain = domain.split('://', 1)[1]
            # Remove paths
            if '/' in domain:
                domain = domain.split('/', 1)[0]
            # Remove ports
            if ':' in domain and not is_ipv6(domain):
                domain = domain.split(':', 1)[0]
                
            if domain and is_valid_domain(domain):
                cleaned.append(domain)
    
    return list(set(cleaned))  # Remove duplicates


def safe_int(value, default: int = 0) -> int:
    """
    Safely convert value to integer with default fallback.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        int: Converted integer or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default: float = 0.0) -> float:
    """
    Safely convert value to float with default fallback.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        float: Converted float or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length with suffix.
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# DNS Record Type Constants
DNS_RECORD_TYPES = {
    'A': 'IPv4 Address',
    'AAAA': 'IPv6 Address', 
    'CNAME': 'Canonical Name',
    'MX': 'Mail Exchange',
    'NS': 'Name Server',
    'TXT': 'Text Record',
    'SOA': 'Start of Authority',
    'PTR': 'Pointer Record',
    'SRV': 'Service Record',
    'CAA': 'Certificate Authority Authorization',
    'DNSKEY': 'DNS Public Key',
    'DS': 'Delegation Signer',
    'RRSIG': 'Resource Record Signature',
    'NSEC': 'Next Secure',
    'NSEC3': 'Next Secure v3'
}

# Common DNS Servers
PUBLIC_DNS_SERVERS = {
    'Google': ['8.8.8.8', '8.8.4.4'],
    'Cloudflare': ['1.1.1.1', '1.0.0.1'],
    'Quad9': ['9.9.9.9', '149.112.112.112'],
    'OpenDNS': ['208.67.222.222', '208.67.220.220'],
    'Verisign': ['64.6.64.6', '64.6.65.6'],
    'Level3': ['4.2.2.1', '4.2.2.2']
}

# IPv6 DNS Servers
PUBLIC_DNS_SERVERS_IPV6 = {
    'Google': ['2001:4860:4860::8888', '2001:4860:4860::8844'],
    'Cloudflare': ['2606:4700:4700::1111', '2606:4700:4700::1001'],
    'Quad9': ['2620:fe::fe', '2620:fe::9'],
    'OpenDNS': ['2620:119:35::35', '2620:119:53::53']
}