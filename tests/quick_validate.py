#!/usr/bin/env python3
"""
Quick validation script
Runs essential checks without full test suite
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.utils.test_helpers import TestHelpers


def main():
    """Run quick validation checks"""
    print("="*60)
    print("FinRobot Quick Validation")
    print("="*60)
    print()
    
    helpers = TestHelpers()
    issues = []
    warnings = []
    
    # Check 1: Mock data imports
    print("1. Checking for mock data imports...")
    finrobot_dir = project_root / 'finrobot'
    for root, dirs, files in os.walk(finrobot_dir):
        if 'test' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                mock_imports = helpers.check_for_mock_imports(file_path)
                if mock_imports:
                    issues.append(f"{file_path}: {mock_imports}")
    
    if issues:
        print(f"   ❌ Found {len(issues)} files with mock imports")
        for issue in issues[:5]:
            print(f"      - {issue}")
    else:
        print("   ✅ No mock data imports found")
    
    print()
    
    # Check 2: Silent failures
    print("2. Checking for silent failure patterns...")
    silent_issues = []
    for root, dirs, files in os.walk(finrobot_dir):
        if 'test' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                    file_issues = helpers.check_silent_fallback(code)
                    if file_issues:
                        silent_issues.extend([f"{file_path}: {issue}" for issue in file_issues])
    
    if silent_issues:
        print(f"   ⚠️  Found {len(silent_issues)} silent failure patterns")
        for issue in silent_issues[:5]:
            print(f"      - {issue}")
    else:
        print("   ✅ No silent failure patterns found")
    
    print()
    
    # Check 3: API keys
    print("3. Checking API key configuration...")
    openai_key = os.environ.get('OPENAI_API_KEY', '')
    finnhub_key = os.environ.get('FINNHUB_API_KEY', '')
    
    if helpers.check_api_key_valid(openai_key):
        print("   ✅ OPENAI_API_KEY is valid")
    else:
        warnings.append("OPENAI_API_KEY not set or invalid")
        print("   ⚠️  OPENAI_API_KEY not set or invalid")
    
    if helpers.check_api_key_valid(finnhub_key):
        print("   ✅ FINNHUB_API_KEY is valid")
    else:
        warnings.append("FINNHUB_API_KEY not set or invalid")
        print("   ⚠️  FINNHUB_API_KEY not set or invalid")
    
    print()
    
    # Check 4: Critical modules importable
    print("4. Checking critical modules are importable...")
    import importlib
    modules = [
        'finrobot.data_source.yfinance_utils',
        'finrobot.functional.analyzer',
        'finrobot.agents.workflow',
    ]
    
    failed = []
    for module_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"   ✅ {module_name}")
        except Exception as e:
            failed.append(f"{module_name}: {e}")
            print(f"   ❌ {module_name}: {e}")
    
    print()
    print("="*60)
    print("Validation Summary")
    print("="*60)
    
    if issues:
        print(f"❌ {len(issues)} critical issues found (mock data)")
    if silent_issues:
        print(f"⚠️  {len(silent_issues)} warnings (silent failures)")
    if warnings:
        print(f"⚠️  {len(warnings)} configuration warnings")
    if failed:
        print(f"❌ {len(failed)} import failures")
    
    if not issues and not failed:
        print("✅ Quick validation passed!")
        return 0
    else:
        print("❌ Quick validation failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())

