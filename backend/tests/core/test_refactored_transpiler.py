#!/usr/bin/env python3
"""
Test Refactored Transpiler
Tests the new clean, scalable transpiler architecture
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_basic_example_1():
    """Basic Example 1: Simple single selection"""
    print("\n--- Basic Example 1: Simple Single Selection ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection': {'EventID': 524},
            'condition': 'selection'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "// log source filter",
        "logsource matches {product: 'windows', service: 'application'};",
        "// event types",
        "safe_selection not matches {eventid: 524};",
        "// property section",
        "Main = logsource >> Monitor;",
        "Monitor = safe_selection*;"
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

def test_basic_example_2():
    """Basic Example 2: Single selection with multiple fields"""
    print("\n--- Basic Example 2: Single Selection with Multiple Fields ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection': {
                'EventID': 524,
                'Provider_Name': 'Microsoft-Windows-Backup'
            },
            'condition': 'selection'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "safe_selection not matches {eventid: 524, provider_name: 'Microsoft-Windows-Backup'};"
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

def test_basic_example_4():
    """Basic Example 4: List values"""
    print("\n--- Basic Example 4: List Values ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': [4728, 4729, 4730]
            },
            'condition': 'selection'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "safe_selection not matches {eventid: 4728 | 4729 | 4730};"
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

def test_basic_example_6():
    """Basic Example 6: NOT condition"""
    print("\n--- Basic Example 6: NOT Condition ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection': {
                'EventID': [4728, 4729, 4730],
                'Provider_Name': 'Microsoft-Windows-Backup'
            },
            'condition': 'not selection'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "safe_selection matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};"
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

def test_basic_example_7():
    """Basic Example 7: AND condition"""
    print("\n--- Basic Example 7: AND Condition ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection_1': {'EventID': 4663},
            'selection_2': {'ObjectName': '\\Device\\CdRom0\\setup.exe'},
            'condition': 'selection_1 and selection_2'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "safe_selection_1 not matches {eventid: 4663};",
        "safe_selection_2 not matches {objectname: '\\Device\\CdRom0\\setup.exe'};",
        "Monitor = (safe_selection_1 /\\ safe_selection_2)*;"
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

def test_basic_example_9():
    """Basic Example 9: OR condition"""
    print("\n--- Basic Example 9: OR Condition ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection_1': {
                'EventID': [4728, 4729, 4730],
                'Provider_Name': 'Microsoft-Windows-Backup'
            },
            'selection_2': {
                'ObjectName': '\\Device\\CdRom0\\setup.exe',
                'FieldName': 'ProcessName'
            },
            'condition': 'selection_1 or selection_2'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "safe_selection_1 not matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};",
        "safe_selection_2 not matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};",
        "Monitor = (safe_selection_1 \\/ safe_selection_2)*;"
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

def test_basic_example_11():
    """Basic Example 11: Numerical modifiers"""
    print("\n--- Basic Example 11: Numerical Modifiers ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection_1': {
                'EventID': [4728, 4729],
                'Provider_Name': 'Microsoft-Windows-Backup',
                'ObjectNumber|gte': 25
            },
            'selection_2': {
                'ObjectName': '\\Device\\CdRom0\\setup.exe',
                'FieldName': 'ProcessName'
            },
            'condition': 'selection_1 or not selection_2'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "objectnumber: x1 with x1 >= 25",
        "safe_selection_2 matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};"
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

def test_basic_example_26():
    """Basic Example 26: Quantifier 'all of'"""
    print("\n--- Basic Example 26: Quantifier 'all of' ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection1': {
                'EventID': 4663,
                'Provider_Name': 'Microsoft-Windows-Backup',
                'ObjectNumber|lte': 100
            },
            'selection2': {
                'ObjectName': '\\Device\\CdRom0\\setup.exe',
                'FieldName': 'ProcessName'
            },
            'condition': 'all of selection*'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Generated:", result)
    
    # Check for expected components
    expected_components = [
        "objectnumber: x1 with x1 <= 100",
        "Monitor = (safe_selection1 /\\ safe_selection2)*;"
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

def test_de_morgan_simplification():
    """Test De Morgan's law simplification"""
    print("\n--- Test De Morgan's Law Simplification ---")
    
    sigma = {
        'detection': {
            'selection': {'Image': 'werfault.exe'},
            'filter1': {'ParentImage': 'svchost.exe'},
            'filter2': {'DestinationIp': '10.0.0.0'},
            'condition': 'selection and not (filter1 or filter2)'
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
        "safe_filter2 matches {destinationip: '10.0.0.0'};"
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
    """Run all test cases"""
    print("TEST: Refactored Transpiler Test Suite")
    print("=" * 100)
    
    tests = [
        test_basic_example_1,
        test_basic_example_2,
        test_basic_example_4,
        test_basic_example_6,
        test_basic_example_7,
        test_basic_example_9,
        test_basic_example_11,
        test_basic_example_26,
        test_de_morgan_simplification
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
    print("This test suite verifies the refactored transpiler architecture")

if __name__ == "__main__":
    run_all_tests()
