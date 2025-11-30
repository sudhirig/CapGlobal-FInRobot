"""
Comprehensive test runner for FinRobot
Runs all tests: unit, integration, UI, API, and validation tests
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_tests(test_type='all', verbose=False, coverage=False, parallel=False):
    """Run tests based on type"""
    
    test_dir = project_root / 'tests'
    
    # Base pytest command
    cmd = ['python', '-m', 'pytest']
    
    if verbose:
        cmd.append('-v')
    else:
        cmd.append('-q')
    
    if coverage:
        cmd.extend(['--cov=finrobot', '--cov-report=html', '--cov-report=term'])
    
    if parallel:
        cmd.extend(['-n', 'auto'])  # Requires pytest-xdist
    
    # Add timeout
    cmd.extend(['--timeout=300'])  # 5 minute timeout per test
    
    # Add HTML report
    cmd.extend(['--html=tests/report.html', '--self-contained-html'])
    
    # Select test type
    if test_type == 'unit':
        cmd.append('tests/unit/')
    elif test_type == 'integration':
        cmd.append('tests/integration/')
    elif test_type == 'ui':
        cmd.append('tests/ui/')
    elif test_type == 'api':
        cmd.append('tests/api/')
    elif test_type == 'all':
        cmd.append('tests/')
    else:
        print(f"Unknown test type: {test_type}")
        return False
    
    print(f"Running {test_type} tests...")
    print(f"Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, cwd=project_root)
    return result.returncode == 0


def check_for_mock_data():
    """Check entire codebase for mock/synthetic data"""
    print("\n" + "="*60)
    print("Checking for mock/synthetic data in codebase...")
    print("="*60)
    
    from tests.utils.test_helpers import TestHelpers
    helpers = TestHelpers()
    
    issues = []
    for root, dirs, files in os.walk(project_root / 'finrobot'):
        # Skip test files and cache
        if 'test' in root or '__pycache__' in root:
            continue
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                mock_imports = helpers.check_for_mock_imports(file_path)
                if mock_imports:
                    issues.append(f"{file_path}: {mock_imports}")
    
    if issues:
        print("⚠️  Mock data libraries found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ No mock data libraries found")
        return True


def check_silent_failures():
    """Check codebase for silent failure patterns"""
    print("\n" + "="*60)
    print("Checking for silent failure patterns...")
    print("="*60)
    
    from tests.utils.test_helpers import TestHelpers
    helpers = TestHelpers()
    
    issues = []
    for root, dirs, files in os.walk(project_root / 'finrobot'):
        if 'test' in root or '__pycache__' in root:
            continue
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                    file_issues = helpers.check_silent_fallback(code)
                    if file_issues:
                        issues.extend([f"{file_path}: {issue}" for issue in file_issues])
    
    if issues:
        print("⚠️  Silent failure patterns found:")
        for issue in issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
        return False
    else:
        print("✅ No silent failure patterns found")
        return True


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description='FinRobot Test Runner')
    parser.add_argument('--type', choices=['all', 'unit', 'integration', 'ui', 'api'],
                       default='all', help='Type of tests to run')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--coverage', '-c', action='store_true',
                       help='Generate coverage report')
    parser.add_argument('--parallel', '-p', action='store_true',
                       help='Run tests in parallel')
    parser.add_argument('--check-mock', action='store_true',
                       help='Check for mock data')
    parser.add_argument('--check-silent', action='store_true',
                       help='Check for silent failures')
    
    args = parser.parse_args()
    
    results = []
    
    # Run code quality checks
    if args.check_mock or args.type == 'all':
        results.append(('Mock Data Check', check_for_mock_data()))
    
    if args.check_silent or args.type == 'all':
        results.append(('Silent Failure Check', check_silent_failures()))
    
    # Run tests
    results.append(('Tests', run_tests(
        test_type=args.type,
        verbose=args.verbose,
        coverage=args.coverage,
        parallel=args.parallel
    )))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name}: {status}")
    
    # Return success if all passed
    return all(result[1] for result in results)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

