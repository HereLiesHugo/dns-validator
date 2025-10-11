"""
DNS Validator - A comprehensive DNS validation tool

This package provides DNS delegation checking, propagation testing,
and provider settings analysis with secure credential management.

Author: Matisse Urquhart
Contact: me@maturqu.com
License: GNU AGPL v3.0
"""

__version__ = "2.7.0"
__author__ = "Matisse Urquhart"

# Import main classes for easy access
from .dns_validator import DNSValidator, cli

# Import modular components for individual use
from . import utils
from . import analytics
from . import bulk
from .api_key_manager import APIKeyManager

__all__ = [
    'DNSValidator', 
    'cli',
    'utils',
    'analytics', 
    'bulk',
    'APIKeyManager'
]