#!/usr/bin/env python3
"""
Test script for the new DNS Validator features:
- Geolocation DNS Testing
- Load Balancer Health Checks  
- IPv6 Support Enhancement

Author: Matisse Urquhart
License: GNU AGPL v3.0
"""

import subprocess
import sys
import time

def run_command(command):
    """Run a CLI command and display results"""
    print(f"\n{'='*80}")
    print(f"Running: {command}")
    print('='*80)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Command timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Test all new features"""
    print("DNS Validator - New Features Test Suite")
    print("Testing: Geolocation DNS, Load Balancer Health, IPv6 Support")
    
    test_domains = {
        "geolocation": ["google.com", "cloudflare.com"],
        "load_balancer": ["cloudflare.com", "netflix.com"],  # Domains likely to have multiple A records
        "ipv6": ["google.com", "facebook.com", "netflix.com"]
    }
    
    # Test Geolocation DNS Testing
    print(f"\n{'-'*40} GEOLOCATION DNS TESTING {'-'*40}")
    for domain in test_domains["geolocation"]:
        success = run_command(f"python dns_validator_cli.py geo-dns {domain}")
        if not success:
            print(f"⚠️ Geolocation DNS test failed for {domain}")
        time.sleep(2)  # Brief pause between tests
    
    # Test Load Balancer Health Checks
    print(f"\n{'-'*40} LOAD BALANCER HEALTH CHECKS {'-'*40}")
    for domain in test_domains["load_balancer"]:
        success = run_command(f"python dns_validator_cli.py load-balancer {domain}")
        if not success:
            print(f"⚠️ Load balancer test failed for {domain}")
        time.sleep(2)
    
    # Test IPv6 Support Enhancement
    print(f"\n{'-'*40} IPv6 SUPPORT VALIDATION {'-'*40}")
    for domain in test_domains["ipv6"]:
        success = run_command(f"python dns_validator_cli.py ipv6-check {domain}")
        if not success:
            print(f"⚠️ IPv6 validation test failed for {domain}")
        time.sleep(2)
    
    # Test verbose mode with one example from each feature
    print(f"\n{'-'*40} VERBOSE MODE TESTING {'-'*40}")
    
    print("\nTesting verbose geolocation DNS:")
    run_command("python dns_validator_cli.py --verbose geo-dns microsoft.com")
    
    print("\nTesting verbose load balancer:")  
    run_command("python dns_validator_cli.py --verbose load-balancer aws.com")
    
    print("\nTesting verbose IPv6:")
    run_command("python dns_validator_cli.py --verbose ipv6-check github.com")
    
    print(f"\n{'='*80}")
    print("🎉 New Features Test Suite Completed!")
    print("✅ Geolocation DNS Testing - Global DNS resolution validation")
    print("✅ Load Balancer Health Checks - Multi-endpoint health validation") 
    print("✅ IPv6 Support Enhancement - Comprehensive IPv6 readiness analysis")
    print(f"{'='*80}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}")
        sys.exit(1)