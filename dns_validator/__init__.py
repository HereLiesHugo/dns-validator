"""
DNS Validator - A comprehensive DNS validation tool

This package provides DNS delegation checking, propagation testing,
and provider settings analysis with secure credential management.
"""

__version__ = "2.0.1"
__author__ = "DNS Validator Team"

# Import main classes for easy access
from .dns_validator import DNSValidator, cli

__all__ = ['DNSValidator', 'cli']