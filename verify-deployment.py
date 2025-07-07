#!/usr/bin/env python3
"""
OpenManus Deployment Verification Script
Checks if the environment is properly configured for deployment.
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 12:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.12+")
        return False

def check_dependencies():
    """Check if required Python packages are available."""
    required_packages = [
        'pydantic',
        'openai', 
        'tenacity',
        'yaml',
        'loguru',
        'fastapi',
        'uvicorn',
        'playwright',
        'aiofiles'
    ]
    
    missing_packages = []
    available_packages = []
    
    for package in required_packages:
        try:
            if package == 'yaml':
                import yaml
            else:
                importlib.import_module(package)
            available_packages.append(package)
        except ImportError:
            missing_packages.append(package)
    
    print(f"✅ Available packages ({len(available_packages)}): {', '.join(available_packages)}")
    if missing_packages:
        print(f"❌ Missing packages ({len(missing_packages)}): {', '.join(missing_packages)}")
        return False
    return True

def check_config_file():
    """Check if config file exists and is properly formatted."""
    config_path = Path("config/config.toml")
    if not config_path.exists():
        print("❌ Config file not found: config/config.toml")
        return False
    
    print("✅ Config file exists: config/config.toml")
    
    # Check if API key is configured
    with open(config_path, 'r') as f:
        content = f.read()
        if 'sk-...' in content:
            print("⚠️  API key placeholder detected - you need to configure real API keys")
            return False
        elif 'api_key = ""' in content or 'your-api-key' in content:
            print("⚠️  API key not configured - you need to add real API keys")
            return False
        else:
            print("✅ API key appears to be configured")
            return True

def check_playwright_browsers():
    """Check if Playwright browsers are installed."""
    try:
        result = subprocess.run(['playwright', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'chromium' in result.stdout:
            print("✅ Playwright browsers installed")
            return True
        else:
            print("❌ Playwright browsers not installed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Playwright not available or browsers not installed")
        return False

def check_file_structure():
    """Check if required files and directories exist."""
    required_paths = [
        'app/',
        'app/agent/',
        'app/agent/manus.py',
        'main.py',
        'requirements.txt',
        'config/',
        'config/config.example.toml'
    ]
    
    missing_paths = []
    for path in required_paths:
        if not Path(path).exists():
            missing_paths.append(path)
    
    if missing_paths:
        print(f"❌ Missing required files/directories: {', '.join(missing_paths)}")
        return False
    else:
        print("✅ All required files and directories present")
        return True

def print_deployment_instructions():
    """Print deployment instructions based on verification results."""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    print()
    print("1. Install dependencies (if missing):")
    print("   pip install -r requirements.txt")
    print()
    print("2. Install Playwright browsers:")
    print("   playwright install chromium")
    print()
    print("3. Configure API keys in config/config.toml:")
    print("   - Replace 'sk-...' with your actual OpenAI API key")
    print("   - Or use Claude API key with appropriate base_url")
    print()
    print("4. Run the application:")
    print("   python main.py")
    print()
    print("5. Alternative: Use the deployment script:")
    print("   ./deploy.sh")
    print()
    print("For detailed instructions, see DEPLOYMENT.md")

def main():
    """Run deployment verification checks."""
    print("🔍 OpenManus Deployment Verification")
    print("="*40)
    
    checks = [
        ("Python Version", check_python_version),
        ("File Structure", check_file_structure),
        ("Dependencies", check_dependencies),
        ("Configuration", check_config_file),
        ("Playwright Browsers", check_playwright_browsers)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            results.append(False)
    
    print("\n" + "="*40)
    print("📊 VERIFICATION SUMMARY")
    print("="*40)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All checks passed ({passed}/{total})!")
        print("✅ OpenManus is ready for deployment!")
    elif passed >= total - 1:
        print(f"⚠️  Most checks passed ({passed}/{total})")
        print("🔧 Minor configuration needed")
    else:
        print(f"❌ Several issues found ({passed}/{total} passed)")
        print("🛠️  Setup required before deployment")
    
    print_deployment_instructions()

if __name__ == "__main__":
    main()