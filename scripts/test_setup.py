#!/usr/bin/env python3
"""
FinRobot Setup Validation Script
Run this to verify your installation and API keys are working.
"""

import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_result(name, success, message=""):
    status = "✅" if success else "❌"
    print(f"{status} {name}: {message}")
    return success

def test_imports():
    """Test that all required packages are installed"""
    print_header("Testing Package Imports")
    
    packages = {
        "autogen": "pyautogen",
        "finnhub": "finnhub-python",
        "yfinance": "yfinance",
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "reportlab": "reportlab",
    }
    
    all_passed = True
    for pkg, pip_name in packages.items():
        try:
            __import__(pkg)
            print_result(pkg, True, "installed")
        except ImportError:
            print_result(pkg, False, f"not found - run: pip install {pip_name}")
            all_passed = False
    
    return all_passed

def test_config_files():
    """Test that config files exist and have proper format"""
    print_header("Testing Configuration Files")
    
    all_passed = True
    
    # Check OAI_CONFIG_LIST
    oai_config = PROJECT_ROOT / "OAI_CONFIG_LIST"
    if oai_config.exists():
        import json
        try:
            with open(oai_config) as f:
                config = json.load(f)
            has_key = any(
                c.get("api_key", "").startswith("sk-") 
                for c in config
            )
            if has_key:
                print_result("OAI_CONFIG_LIST", True, "valid API key found")
            else:
                print_result("OAI_CONFIG_LIST", False, "no valid API key (should start with 'sk-')")
                all_passed = False
        except json.JSONDecodeError:
            print_result("OAI_CONFIG_LIST", False, "invalid JSON format")
            all_passed = False
    else:
        print_result("OAI_CONFIG_LIST", False, "file not found")
        all_passed = False
    
    # Check config_api_keys
    api_keys = PROJECT_ROOT / "config_api_keys"
    if api_keys.exists():
        import json
        try:
            with open(api_keys) as f:
                keys = json.load(f)
            required = ["FINNHUB_API_KEY", "FMP_API_KEY"]
            missing = [k for k in required if keys.get(k, "").startswith("YOUR_")]
            if not missing:
                print_result("config_api_keys", True, "API keys configured")
            else:
                print_result("config_api_keys", False, f"missing: {', '.join(missing)}")
                all_passed = False
        except json.JSONDecodeError:
            print_result("config_api_keys", False, "invalid JSON format")
            all_passed = False
    else:
        print_result("config_api_keys", False, "file not found")
        all_passed = False
    
    return all_passed

def test_yfinance():
    """Test YFinance data retrieval (no API key needed)"""
    print_header("Testing YFinance (No API Key Required)")
    
    try:
        from finrobot.data_source import YFinanceUtils
        data = YFinanceUtils.get_stock_data("AAPL", "2024-01-01", "2024-01-05")
        if len(data) > 0:
            print_result("YFinance", True, f"retrieved {len(data)} rows for AAPL")
            print(f"   Sample: {data['Close'].iloc[0]:.2f} (closing price)")
            return True
        else:
            print_result("YFinance", False, "no data returned")
            return False
    except Exception as e:
        print_result("YFinance", False, str(e))
        return False

def test_finnhub():
    """Test Finnhub API connection"""
    print_header("Testing Finnhub API")
    
    try:
        from finrobot.utils import register_keys_from_json
        from finrobot.data_source import FinnHubUtils
        
        register_keys_from_json(str(PROJECT_ROOT / "config_api_keys"))
        profile = FinnHubUtils.get_company_profile("AAPL")
        
        if profile and "Apple" in profile:
            print_result("Finnhub", True, "company profile retrieved")
            return True
        elif "Please set" in str(profile):
            print_result("Finnhub", False, "API key not configured")
            return False
        else:
            print_result("Finnhub", False, f"unexpected response: {profile[:100]}")
            return False
    except Exception as e:
        print_result("Finnhub", False, str(e))
        return False

def test_fmp():
    """Test Financial Modeling Prep API"""
    print_header("Testing FMP API")
    
    try:
        from finrobot.utils import register_keys_from_json
        from finrobot.data_source import FMPUtils
        
        register_keys_from_json(str(PROJECT_ROOT / "config_api_keys"))
        report = FMPUtils.get_sec_report("AAPL", "2023")
        
        if report and "Link:" in report:
            print_result("FMP", True, "SEC report URL retrieved")
            return True
        elif "Please set" in str(report):
            print_result("FMP", False, "API key not configured")
            return False
        else:
            print_result("FMP", False, f"unexpected response: {report[:100]}")
            return False
    except Exception as e:
        print_result("FMP", False, str(e))
        return False

def test_openai():
    """Test OpenAI API configuration"""
    print_header("Testing OpenAI Configuration")
    
    try:
        import autogen
        config_list = autogen.config_list_from_json(
            str(PROJECT_ROOT / "OAI_CONFIG_LIST"),
            filter_dict={"model": ["gpt-4-0125-preview", "gpt-4-turbo", "gpt-4o", "gpt-4"]}
        )
        
        if len(config_list) > 0:
            print_result("OpenAI Config", True, f"found {len(config_list)} model(s)")
            for cfg in config_list:
                model = cfg.get("model", "unknown")
                key_preview = cfg.get("api_key", "")[:10] + "..."
                print(f"   - {model} (key: {key_preview})")
            return True
        else:
            print_result("OpenAI Config", False, "no valid configurations found")
            return False
    except Exception as e:
        print_result("OpenAI Config", False, str(e))
        return False

def main():
    print("\n" + "🤖 " * 20)
    print("    FINROBOT SETUP VALIDATION")
    print("🤖 " * 20)
    
    results = {
        "Package Imports": test_imports(),
        "Config Files": test_config_files(),
        "YFinance": test_yfinance(),
        "Finnhub": test_finnhub(),
        "FMP": test_fmp(),
        "OpenAI": test_openai(),
    }
    
    print_header("SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test}: {status}")
    
    print(f"\n  Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 All systems go! You're ready to use FinRobot!")
    else:
        print("\n  ⚠️  Some tests failed. Please fix the issues above.")
        print("  📖 See IMPLEMENTATION_GUIDE.md for setup instructions.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

