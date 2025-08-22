#!/usr/bin/env python3
"""
Comprehensive Test for Refactored Transpiler
Tests the refactored transpiler with complex examples from examples.txt
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_complex_parentheses():
    """Test complex parenthesized conditions"""
    print("\n--- Complex Parentheses Test ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection1': {'EventID': 4663},
            'selection2': {'ObjectName': '\\Device\\CdRom0\\setup.exe'},
            'selection3': {'FieldName': 'ProcessName'},
            'condition': 'selection1 and (selection2 or selection3)'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "safe_selection1 not matches {eventid: 4663};",
        "safe_selection2 not matches {objectname: '\\Device\\CdRom0\\setup.exe'};",
        "safe_selection3 not matches {fieldname: 'ProcessName'};",
        "Monitor = (safe_selection1 /\\ safe_selection2 /\\ safe_selection3)*;"
    ]
    
    all_found = True
    for component in expected_components:
        if component in result:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            all_found = False
    
    print("Match:", "✅ PASS" if all_found else "❌ FAIL")
    return all_found

def test_nested_not_conditions():
    """Test deeply nested NOT conditions"""
    print("\n--- Nested NOT Conditions Test ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {'Image': 'werfault.exe'},
            'filter1': {'ParentImage': 'svchost.exe'},
            'filter2': {'DestinationIp': '10.0.0.0'},
            'filter3': {'ProcessName': 'explorer.exe'},
            'condition': 'selection and not (filter1 or (filter2 and not filter3))'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "safe_selection not matches {image: 'werfault.exe'};",
        "safe_filter1 matches {parentimage: 'svchost.exe'};",
        "safe_filter2 matches {destinationip: '10.0.0.0'};",
        "safe_filter3 not matches {processname: 'explorer.exe'};"
    ]
    
    all_found = True
    for component in expected_components:
        if component in result:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            all_found = False
    
    print("Match:", "✅ PASS" if all_found else "❌ FAIL")
    return all_found

def test_multiple_numerical_modifiers():
    """Test multiple selections with numerical modifiers"""
    print("\n--- Multiple Numerical Modifiers Test ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection1': {
                'EventID': 4663,
                'ObjectNumber|gte': 25,
                'Count|lt': 100
            },
            'selection2': {
                'ProcessId|gt': 1000,
                'ThreadId|lte': 5000
            },
            'condition': 'selection1 and selection2'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "objectnumber: x1 with x1 >= 25",
        "count: x2 with x2 < 100",
        "processid: x3 with x3 > 1000",
        "threadid: x4 with x4 <= 5000"
    ]
    
    all_found = True
    for component in expected_components:
        if component in result:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            all_found = False
    
    print("Match:", "✅ PASS" if all_found else "❌ FAIL")
    return all_found

def test_quantifier_variations():
    """Test various quantifier patterns"""
    print("\n--- Quantifier Variations Test ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection1': {'EventID': 4663},
            'selection2': {'ObjectName': '\\Device\\CdRom0\\setup.exe'},
            'selection3': {'FieldName': 'ProcessName'},
            'condition': 'any of selection*'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "Monitor = (safe_selection1 \\/ safe_selection2 \\/ safe_selection3)*;"
    ]
    
    all_found = True
    for component in expected_components:
        if component in result:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            all_found = False
    
    print("Match:", "✅ PASS" if all_found else "❌ FAIL")
    return all_found

def test_unsupported_quantifier():
    """Test unsupported quantifier patterns"""
    print("\n--- Unsupported Quantifier Test ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection1': {'EventID': 4663},
            'selection2': {'ObjectName': '\\Device\\CdRom0\\setup.exe'},
            'condition': '2 of selection*'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "Monitor = UNSUPPORTED_PATTERN; // 2 of selection* not supported"
    ]
    
    all_found = True
    for component in expected_components:
        if component in result:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            all_found = False
    
    print("Match:", "✅ PASS" if all_found else "❌ FAIL")
    return all_found

def test_mixed_conditions():
    """Test mixed AND/OR/NOT conditions"""
    print("\n--- Mixed Conditions Test ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection1': {'EventID': 4663},
            'selection2': {'ObjectName': '\\Device\\CdRom0\\setup.exe'},
            'selection3': {'FieldName': 'ProcessName'},
            'selection4': {'Image': 'werfault.exe'},
            'condition': '(selection1 or selection2) and not (selection3 and selection4)'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "safe_selection1 not matches {eventid: 4663};",
        "safe_selection2 not matches {objectname: '\\Device\\CdRom0\\setup.exe'};",
        "safe_selection3 matches {fieldname: 'ProcessName'};",
        "safe_selection4 matches {image: 'werfault.exe'};"
    ]
    
    all_found = True
    for component in expected_components:
        if component in result:
            print(f"✅ Found: {component}")
        else:
            print(f"❌ Missing: {component}")
            all_found = False
    
    print("Match:", "✅ PASS" if all_found else "❌ FAIL")
    return all_found

def run_all_tests():
    """Run all comprehensive test cases"""
    print("TEST: Comprehensive Refactored Transpiler Test Suite")
    print("=" * 100)
    
    tests = [
        test_complex_parentheses,
        test_nested_not_conditions,
        test_multiple_numerical_modifiers,
        test_quantifier_variations,
        test_unsupported_quantifier,
        test_mixed_conditions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 100)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("This comprehensive test suite verifies complex Sigma rule handling")

if __name__ == "__main__":
    run_all_tests()
