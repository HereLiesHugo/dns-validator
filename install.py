#!/usr/bin/env python3
"""
Simple installation script for DNS Validator
Cross-platform installer for Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python 3.7+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    dependencies = [
        "click>=8.0.0",
        "dnspython>=2.3.0", 
        "requests>=2.28.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "pycryptodome>=3.15.0"
    ]
    
    print("📦 Installing dependencies...")
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Installing {dep.split('>=')[0]}"):
            return False
    return True

def make_executable():
    """Make the script executable on Unix systems"""
    if platform.system() != "Windows":
        return run_command("chmod +x dns_validator.py", "Making script executable")
    return True

def create_batch_file():
    """Create a batch file for Windows users"""
    if platform.system() == "Windows":
        batch_content = f"""@echo off
python "{os.path.abspath('dns_validator.py')}" %*
"""
        try:
            with open("dns-validator.bat", "w") as f:
                f.write(batch_content)
            print("✅ Created dns-validator.bat for easy Windows usage")
            return True
        except Exception as e:
            print(f"⚠️  Could not create batch file: {e}")
    return True

def create_shell_script():
    """Create a shell script for Unix systems"""
    if platform.system() != "Windows":
        script_content = f"""#!/bin/bash
python3 "{os.path.abspath('dns_validator.py')}" "$@"
"""
        try:
            with open("dns-validator", "w") as f:
                f.write(script_content)
            os.chmod("dns-validator", 0o755)
            print("✅ Created dns-validator shell script")
            return True
        except Exception as e:
            print(f"⚠️  Could not create shell script: {e}")
    return True

def main():
    """Main installation function"""
    print("🚀 DNS Validator Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please try manual installation:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Make executable
    make_executable()
    
    # Create convenience scripts
    create_batch_file()
    create_shell_script()
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Usage Instructions:")
    print("=" * 30)
    
    if platform.system() == "Windows":
        print("Windows Usage:")
        print("  python dns_validator.py delegation example.com")
        print("  OR")
        print("  dns-validator.bat delegation example.com")
    else:
        print("Linux/macOS Usage:")
        print("  python3 dns_validator.py delegation example.com")
        print("  OR")
        print("  ./dns-validator delegation example.com")
    
    print("\n🔍 Available Commands:")
    print("  delegation    - Check DNS delegation")
    print("  propagation   - Check DNS propagation")
    print("  cloudflare    - Check Cloudflare settings")
    print("  full          - Run all checks")
    print("  --verbose     - Enable detailed output")
    
    print("\n📖 For more help:")
    print("  python dns_validator.py --help")

if __name__ == "__main__":
    main()