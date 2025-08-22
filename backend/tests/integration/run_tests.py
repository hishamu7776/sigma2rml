#!/usr/bin/env python3
"""
Comprehensive test runner for Sigma to RML Transpiler
Runs all test categories and provides a detailed summary
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
            return True, "PASS: Passed"
        else:
            return False, f"FAIL: Failed: {result.stderr.strip()}"
    except Exception as e:
        return False, f"FAIL: Failed: {str(e)}"

def main():
    """Run all test files and provide comprehensive summary"""
    print("TEST: Running Comprehensive Sigma to RML Transpiler Tests")
    print("=" * 80)
    
    # Test files organized by category
    test_categories = {
        "Core Transpiler Tests": [
            'tests/test_basic_patterns.py',
            'tests/test_numerical_modifiers.py',
            'tests/test_complex_conditions.py',
            'tests/test_temporal_operators.py',
            'tests/test_quantifiers.py',
            'tests/test_unsupported_modifiers.py',
            'tests/test_transpiler.py'
        ],
        "Basic Pattern Tests": [
            'test_basic_patterns_comprehensive.py'
        ],
        "Temporal Monitor Tests": [
            'test_enhanced_temporal.py',
            'test_fixed_temporal.py',
            'test_near_operator.py'
        ],
        "API Tests": [
            'test_apis.py',
            'test_improved_apis.py',
            'test_rml_endpoint.py'
        ],
        "Integration Tests": [
            'test_path_fix.py',
            'test_final_validation.py'
        ]
    }
    
    all_results = []
    category_results = {}
    
    for category, test_files in test_categories.items():
        print(f"\nVERIFY: {category}")
        print("-" * 50)
        
        category_results[category] = []
        
        for test_file in test_files:
            test_path = os.path.join(os.path.dirname(__file__), test_file)
            if os.path.exists(test_path):
                print(f"RUNNING: Running {os.path.basename(test_file)}...")
                success, message = run_test_file(test_path)
                result = (os.path.basename(test_file), success, message)
                category_results[category].append(result)
                all_results.append(result)
                print(f"   {message}")
            else:
                print(f"FAIL: Test file not found: {test_file}")
                result = (os.path.basename(test_file), False, "File not found")
                category_results[category].append(result)
                all_results.append(result)
    
    # Print detailed summary
    print("\n" + "=" * 80)
    print("SUMMARY: COMPREHENSIVE TEST SUMMARY")
    print("=" * 80)
    
    total_passed = 0
    total_failed = 0
    
    for category, results in category_results.items():
        print(f"\nCATEGORY: {category}")
        print("-" * 40)
        
        category_passed = 0
        category_failed = 0
        
        for test_file, success, message in results:
            status = "PASS" if success else "FAIL"
            print(f"  {status} {test_file}")
            if success:
                category_passed += 1
                total_passed += 1
            else:
                category_failed += 1
                total_failed += 1
        
        print(f"  SUMMARY: Category Summary: {category_passed} passed, {category_failed} failed")
    
    # Overall summary
    print("\n" + "=" * 80)
    print("RESULT: OVERALL SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(all_results)}")
    print(f"PASS: Total Passed: {total_passed}")
    print(f"FAIL: Total Failed: {total_failed}")
    
    if total_failed == 0:
        print("\nSUCCESS: All tests passed! The transpiler is working correctly.")
    else:
        print(f"\nWARNING: {total_failed} test(s) failed. Please check the output above.")
        print("\nRECOMMEND: Recommended actions:")
        print("   - Check error messages for failed tests")
        print("   - Verify that recent changes haven't broken existing functionality")
        print("   - Run individual failed tests to debug specific issues")
    
    return total_failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
