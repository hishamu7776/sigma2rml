#!/usr/bin/env python3
"""
Simple test runner for Sigma to RML Transpiler
Runs all test categories and provides a summary
"""

import sys
import os
import subprocess

def run_test_file(test_file):
    """Run a single test file and return results"""
    try:
        # Run the test file as a subprocess
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(test_file)
        )
        
        if result.returncode == 0:
            return True, "✅ Passed"
        else:
            return False, f"❌ Failed: {result.stderr.strip()}"
    except Exception as e:
        return False, f"❌ Failed: {str(e)}"

def main():
    """Run all test files and provide summary"""
    print("🧪 Running Sigma to RML Transpiler Tests")
    print("=" * 60)
    
    # Get the tests directory
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    # List of test files to run
    test_files = [
        'test_basic_patterns.py',
        'test_numerical_modifiers.py',
        'test_complex_conditions.py',
        'test_temporal_operators.py',
        'test_quantifiers.py',
        'test_unsupported_modifiers.py',
        'test_transpiler.py'
    ]
    
    results = []
    
    for test_file in test_files:
        test_path = os.path.join(tests_dir, test_file)
        if os.path.exists(test_path):
            print(f"\n📋 Running {test_file}...")
            success, message = run_test_file(test_path)
            results.append((test_file, success, message))
            print(f"   {message}")
        else:
            print(f"\n❌ Test file not found: {test_file}")
            results.append((test_file, False, "File not found"))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_file, success, message in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_file}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"🎯 Total Tests: {len(results)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! The transpiler is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the output above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
