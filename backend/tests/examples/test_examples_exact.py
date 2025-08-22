#!/usr/bin/env python3
"""
Exact Examples Test Suite for Sigma to RML Transpiler
Uses corrected examples that match the Sigma-to-RML semantic mapping
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
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection not matches {eventid: 524};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

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
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection not matches {eventid: 524, provider_name: 'Microsoft-Windows-Backup'};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

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
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'security'};

// event types
safe_selection not matches {eventid: 4728 | 4729 | 4730};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

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
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

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
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection_1 not matches {eventid: 4663};
safe_selection_2 not matches {objectname: '\\Device\\CdRom0\\setup.exe'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 \\/ safe_selection_2)*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

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
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection_1 not matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};
safe_selection_2 not matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 /\\ safe_selection_2)*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

def test_basic_example_10():
    """Basic Example 10: NOT with OR"""
    print("\n--- Basic Example 10: NOT with OR ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection_1': {
                'EventID': [4728, 4729, 4730],
                'Provider_Name': 'Microsoft-Windows-Backup',
                'ObjectCategory': 'Create',
                'OptionalFields': ['TargetObject', 'ProcessId']
            },
            'selection_2': {
                'ObjectName': '\\Device\\CdRom0\\setup.exe',
                'FieldName': 'ProcessName'
            },
            'condition': 'not selection_1 or selection_2'
        }
    }
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection_1 matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup', objectcategory: 'Create', optionalfields: 'TargetObject' | 'ProcessId'};
safe_selection_2 not matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 /\\ safe_selection_2)*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

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
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection_1 not matches {eventid: 4728 | 4729, provider_name: 'Microsoft-Windows-Backup', objectnumber: x1 with x1 >= 25};
safe_selection_2 matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 /\\ safe_selection_2)*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

def test_basic_example_16():
    """Basic Example 16: Parenthesized condition"""
    print("\n--- Basic Example 16: Parenthesized Condition ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection1': {'EventID': 4663},
            'selection2': {'EventName': 'ProcessName'},
            'selection3': {'FieldName': 'something'},
            'condition': 'selection1 and (selection2 or selection3)'
        }
    }
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection1 not matches {eventid: 4663};
safe_selection2 not matches {eventname: 'ProcessName'};
safe_selection3 not matches {fieldname: 'something'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection1 /\\ safe_selection2 /\\ safe_selection3)*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

def test_basic_example_22():
    """Basic Example 22: Complex NOT with parentheses"""
    print("\n--- Basic Example 22: Complex NOT with Parentheses ---")
    
    sigma = {
        'logsource': {'product': 'windows', 'service': 'edr'},
        'detection': {
            'selection': {'image': 'werfault.exe'},
            'filter1': {'parentimage': 'svchost.exe'},
            'filter2': {'destinationip': ['10.0.0.0', '172.16.0.0', '192.168.0.0']},
            'filter3': {'destinationhostname': ['windowsupdate.com', 'microsoft.com']},
            'condition': 'selection and not ( filter1 or filter2 or filter3 )'
        }
    }
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'edr'};

// event types
safe_selection not matches {image: 'werfault.exe'};
safe_filter1 matches {parentimage: 'svchost.exe'};
safe_filter2 matches {destinationip: '10.0.0.0' | '172.16.0.0' | '192.168.0.0'};
safe_filter3 matches {destinationhostname: 'windowsupdate.com' | 'microsoft.com'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection /\\ safe_filter1 /\\ safe_filter2 /\\ safe_filter3)*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

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
    
    expected = """// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection1 not matches {eventid: 4663, provider_name: 'Microsoft-Windows-Backup', objectnumber: x1 with x1 <= 100};
safe_selection2 not matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection1 /\\ safe_selection2)*;"""
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("Input:", sigma['detection']['condition'])
    print("Expected:", expected)
    print("Generated:", result)
    print("Match:", "✅ PASS" if result.strip() == expected.strip() else "❌ FAIL")
    return result.strip() == expected.strip()

def main():
    """Run all tests"""
    print("TEST: Corrected Examples Test Suite")
    print("=" * 80)
    
    tests = [
        test_basic_example_1,
        test_basic_example_2,
        test_basic_example_4,
        test_basic_example_6,
        test_basic_example_7,
        test_basic_example_9,
        test_basic_example_10,
        test_basic_example_11,
        test_basic_example_16,
        test_basic_example_22,
        test_basic_example_26
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 80)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("This test suite uses corrected Sigma-to-RML semantic mapping")
    print("OR conditions in Sigma become AND in RML (both must be satisfied for safety)")
    print("AND conditions in Sigma become OR in RML (either violation makes it unsafe)")

if __name__ == "__main__":
    main()
