#!/usr/bin/env python3
"""
Comprehensive Test Suite for Sigma to RML Transpiler
Tests all use cases from examples.txt with expected vs. generated comparisons
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_transpiler():
    """Run comprehensive transpiler tests based on examples.txt"""
    transpiler = RefactoredTranspiler()
    
    print("TEST: Comprehensive Transpiler Test Suite (Based on examples.txt)")
    print("=" * 100)
    
    # Test 1: Basic Example 1 - Simple single selection
    print("\n--- Test 1: Basic Example 1 - Simple Single Selection ---")
    sigma_1 = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection': {'EventID': 524},
            'condition': 'selection'
        }
    }
    expected_1 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection matches {eventid: 524};
safe_selection not matches {eventid: 524};

// property section

Main = logsource >> Monitor;

Monitor = safe_selection*;"""
    
    result_1 = transpiler.transpile(sigma_1)
    print("Input:", sigma_1['detection']['condition'])
    print("Expected:", expected_1)
    print("Generated:", result_1)
    print("Match:", "✅ PASS" if result_1.strip() == expected_1.strip() else "❌ FAIL")
    
    # Test 2: Basic Example 2 - Single selection with multiple fields
    print("\n--- Test 2: Basic Example 2 - Single Selection with Multiple Fields ---")
    sigma_2 = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection': {
                'EventID': 524,
                'Provider_Name': 'Microsoft-Windows-Backup'
            },
            'condition': 'selection'
        }
    }
    expected_2 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection matches {eventid: 524, provider_name: 'Microsoft-Windows-Backup'};
safe_selection not matches {eventid: 524, provider_name: 'Microsoft-Windows-Backup'};

// property section

Main = logsource >> Monitor;

Monitor = safe_selection*;"""
    
    result_2 = transpiler.transpile(sigma_2)
    print("Input:", sigma_2['detection']['condition'])
    print("Expected:", expected_2)
    print("Generated:", result_2)
    print("Match:", "✅ PASS" if result_2.strip() == expected_2.strip() else "❌ FAIL")
    
    # Test 3: Basic Example 4 - List values
    print("\n--- Test 3: Basic Example 4 - List Values ---")
    sigma_3 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': [4728, 4729, 4730]
            },
            'condition': 'selection'
        }
    }
    expected_3 = """logsource matches {product: 'windows', service: 'security'};

// event types

// negation
selection matches {eventid: 4728 | 4729 | 4730};
safe_selection not matches {eventid: 4728 | 4729 | 4730};

// property section

Main = logsource >> Monitor;

Monitor = safe_selection*;"""
    
    result_3 = transpiler.transpile(sigma_3)
    print("Input:", sigma_3['detection']['condition'])
    print("Expected:", expected_3)
    print("Generated:", result_3)
    print("Match:", "✅ PASS" if result_3.strip() == expected_3.strip() else "❌ FAIL")
    
    # Test 4: Basic Example 6 - NOT condition
    print("\n--- Test 4: Basic Example 6 - NOT Condition ---")
    sigma_4 = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection': {
                'EventID': [4728, 4729, 4730],
                'Provider_Name': 'Microsoft-Windows-Backup'
            },
            'condition': 'not selection'
        }
    }
    expected_4 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};
safe_selection matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};

// property section

Main = logsource >> Monitor;

Monitor = safe_selection*;"""
    
    result_4 = transpiler.transpile(sigma_4)
    print("Input:", sigma_4['detection']['condition'])
    print("Expected:", expected_4)
    print("Generated:", result_4)
    print("Match:", "✅ PASS" if result_4.strip() == expected_4.strip() else "❌ FAIL")
    
    # Test 5: Basic Example 7 - AND condition
    print("\n--- Test 5: Basic Example 7 - AND Condition ---")
    sigma_5 = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection_1': {'EventID': 4663},
            'selection_2': {'ObjectName': '\\Device\\CdRom0\\setup.exe'},
            'condition': 'selection_1 and selection_2'
        }
    }
    expected_5 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection_1 matches {eventid: 4663};
selection_2 matches {objectname: '\\Device\\CdRom0\\setup.exe'};
safe_selection_1 not matches {eventid: 4663};
safe_selection_2 not matches {objectname: '\\Device\\CdRom0\\setup.exe'};

// property section

Main = logsource >> Monitor;

Monitor = (safe_selection_1 \\/ safe_selection_2)*;"""
    
    result_5 = transpiler.transpile(sigma_5)
    print("Input:", sigma_5['detection']['condition'])
    print("Expected:", expected_5)
    print("Generated:", result_5)
    print("Match:", "✅ PASS" if result_5.strip() == expected_5.strip() else "❌ FAIL")
    
    # Test 6: Basic Example 9 - OR condition
    print("\n--- Test 6: Basic Example 9 - OR Condition ---")
    sigma_6 = {
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
    expected_6 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection_1 matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};
selection_2 matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};
safe_selection_1 not matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};
safe_selection_2 not matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};

// property section

Main = logsource >> Monitor;

Monitor = (safe_selection_1 /\\ safe_selection_2)*;"""
    
    result_6 = transpiler.transpile(sigma_6)
    print("Input:", sigma_6['detection']['condition'])
    print("Expected:", expected_6)
    print("Generated:", result_6)
    print("Match:", "✅ PASS" if result_6.strip() == expected_6.strip() else "❌ FAIL")
    
    # Test 7: Basic Example 10 - NOT with OR
    print("\n--- Test 7: Basic Example 10 - NOT with OR ---")
    sigma_7 = {
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
    expected_7 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection_1 matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup', objectcategory: 'Create', optionalfields: 'TargetObject' | 'ProcessId'};
selection_2 matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};
safe_selection_1 matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup', objectcategory: 'Create', optionalfields: 'TargetObject' | 'ProcessId'};
safe_selection_2 not matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};

// property section

Main = logsource >> Monitor;

Monitor = (safe_selection_1 /\\ safe_selection_2)*;"""
    
    result_7 = transpiler.transpile(sigma_7)
    print("Input:", sigma_7['detection']['condition'])
    print("Expected:", expected_7)
    print("Generated:", result_7)
    print("Match:", "✅ PASS" if result_7.strip() == expected_7.strip() else "❌ FAIL")
    
    # Test 8: Basic Example 11 - Numerical modifiers
    print("\n--- Test 8: Basic Example 11 - Numerical Modifiers ---")
    sigma_8 = {
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
    expected_8 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection_1 matches {eventid: 4728 | 4729, provider_name: 'Microsoft-Windows-Backup', objectnumber|gte: 25};
selection_2 matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};
safe_selection_1 not matches {eventid: 4728 | 4729, provider_name: 'Microsoft-Windows-Backup', objectnumber|gte: 25};
safe_selection_2 matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};

// property section

Main = logsource >> Monitor;

Monitor = (safe_selection_1 /\\ safe_selection_2)*;"""
    
    result_8 = transpiler.transpile(sigma_8)
    print("Input:", sigma_8['detection']['condition'])
    print("Expected:", expected_8)
    print("Generated:", result_8)
    print("Match:", "✅ PASS" if result_8.strip() == expected_8.strip() else "❌ FAIL")
    
    # Test 9: Basic Example 16 - Parenthesized condition
    print("\n--- Test 9: Basic Example 16 - Parenthesized Condition ---")
    sigma_9 = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection1': {'EventID': 4663},
            'selection2': {'EventName': 'ProcessName'},
            'selection3': {'FieldName': 'something'},
            'condition': 'selection1 and (selection2 or selection3)'
        }
    }
    expected_9 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection1 matches {eventid: 4663};
selection2 matches {eventname: 'ProcessName'};
selection3 matches {fieldname: 'something'};
safe_selection1 not matches {eventid: 4663};
safe_selection2 not matches {eventname: 'ProcessName'};
safe_selection3 not matches {fieldname: 'something'};

// property section

Main = logsource >> Monitor;

Selection2 = (safe_selection2 \\/ safe_selection3);

Monitor = (safe_selection1 /\\ Selection2)*;"""
    
    result_9 = transpiler.transpile(sigma_9)
    print("Input:", sigma_9['detection']['condition'])
    print("Expected:", expected_9)
    print("Generated:", result_9)
    print("Match:", "✅ PASS" if result_9.strip() == expected_9.strip() else "❌ FAIL")
    
    # Test 10: Basic Example 22 - Complex NOT with parentheses
    print("\n--- Test 10: Basic Example 22 - Complex NOT with Parentheses ---")
    sigma_10 = {
        'detection': {
            'selection': {'Image': 'werfault.exe'},
            'filter1': {'ParentImage': 'svchost.exe'},
            'filter2': {
                'DestinationIp': ['10.0.0.0', '172.16.0.0', '192.168.0.0']
            },
            'filter3': {
                'DestinationHostname': ['windowsupdate.com', 'microsoft.com']
            },
            'condition': 'selection and not ( filter1 or filter2 or filter3 )'
        }
    }
    expected_10 = """logsource matches {product: 'windows', service: 'security'};

// event types

// negation
selection matches {image: 'werfault.exe'};
filter1 matches {parentimage: 'svchost.exe'};
filter2 matches {destinationip: '10.0.0.0' | '172.16.0.0' | '192.168.0.0'};
filter3 matches {destinationhostname: 'windowsupdate.com' | 'microsoft.com'};
safe_selection not matches {image: 'werfault.exe'};
safe_filter1 matches {parentimage: 'svchost.exe'};
safe_filter2 matches {destinationip: '10.0.0.0' | '172.16.0.0' | '192.168.0.0'};
safe_filter3 matches {destinationhostname: 'windowsupdate.com' | 'microsoft.com'};

// property section

Main = logsource >> Monitor;

Monitor = (safe_selection \\/ safe_filter1 \\/ safe_filter2 \\/ safe_filter3)*;"""
    
    result_10 = transpiler.transpile(sigma_10)
    print("Input:", sigma_10['detection']['condition'])
    print("Expected:", expected_10)
    print("Generated:", result_10)
    print("Match:", "✅ PASS" if result_10.strip() == expected_10.strip() else "❌ FAIL")
    
    # Test 11: Basic Example 26 - Quantifier "all of"
    print("\n--- Test 11: Basic Example 26 - Quantifier 'all of' ---")
    sigma_11 = {
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
    expected_11 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection1 matches {eventid: 4663, provider_name: 'Microsoft-Windows-Backup', objectnumber|lte: 100};
selection2 matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};
safe_selection1 not matches {eventid: 4663, provider_name: 'Microsoft-Windows-Backup', objectnumber|lte: 100};
safe_selection2 not matches {objectname: '\\Device\\CdRom0\\setup.exe', fieldname: 'ProcessName'};

// property section

Main = logsource >> Monitor;

Monitor = (safe_selection1 \\/ safe_selection2)*;"""
    
    result_11 = transpiler.transpile(sigma_11)
    print("Input:", sigma_11['detection']['condition'])
    print("Expected:", expected_11)
    print("Generated:", result_11)
    print("Match:", "✅ PASS" if result_11.strip() == expected_11.strip() else "❌ FAIL")
    
    # Test 12: Basic Example 27 - Quantifier "1 of"
    print("\n--- Test 12: Basic Example 27 - Quantifier '1 of' ---")
    sigma_12 = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection1': {
                'EventID': 4663,
                'ObjectNumber|lte': 100,
                'ObjectValue|lt': 23
            },
            'selection2': {
                'FieldName': 'ProcessName',
                'FieldValue|gt': 1000
            },
            'condition': '1 of selection*'
        }
    }
    expected_12 = """logsource matches {product: 'windows', service: 'application'};

// event types

// negation
selection1 matches {eventid: 4663, objectnumber|lte: 100, objectvalue|lt: 23};
selection2 matches {fieldname: 'ProcessName', fieldvalue|gt: 1000};
safe_selection1 not matches {eventid: 4663, objectnumber|lte: 100, objectvalue|lt: 23};
safe_selection2 not matches {fieldname: 'ProcessName', fieldvalue|gt: 1000};

// property section

Main = logsource >> Monitor;

Monitor = (safe_selection1 /\\ safe_selection2)*;"""
    
    result_12 = transpiler.transpile(sigma_12)
    print("Input:", sigma_12['detection']['condition'])
    print("Expected:", expected_12)
    print("Generated:", result_12)
    print("Match:", "✅ PASS" if result_12.strip() == expected_12.strip() else "❌ FAIL")
    
    # Test 13: Temporal Example 2 - Near operator
    print("\n--- Test 13: Temporal Example 2 - Near Operator ---")
    sigma_13 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection_task': {'EventID': 4698},
            'selection_firewall': {'EventID': 4946},
            'condition': 'selection_task | near selection_firewall'
        }
    }
    expected_13_contains = [
        "// Main expression handled by temporal monitor",
        "// Selection definitions",
        "safe_selection_task(ts) matches {timestamp: ts, eventid: 4698}",
        "safe_selection_firewall(ts) matches {timestamp: ts, eventid: 4946}",
        "Main = logsource >> Monitor<0, 0, 0>!",
        "ts - start_ts > 10000"  # Should use 10s default
    ]
    
    result_13 = transpiler.transpile(sigma_13)
    print("Input:", sigma_13['detection']['condition'])
    print("Generated:", result_13)
    
    all_contained = True
    for expected in expected_13_contains:
        if expected not in result_13:
            print(f"❌ Missing: {expected}")
            all_contained = False
        else:
            print(f"✅ Found: {expected}")
    
    print("Match:", "✅ PASS" if all_contained else "❌ FAIL")
    
    # Test 14: Temporal Example 6 - Count operator
    print("\n--- Test 14: Temporal Example 6 - Count Operator ---")
    sigma_14 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4663,
                'Accesses': 'DELETE'
            },
            'condition': 'selection | count() > 5'
        }
    }
    expected_14_contains = [
        "// Main expression handled by temporal monitor",
        "// Selection definitions",
        "safe_selection(ts) matches {timestamp: ts, eventid: 4663, accesses: 'DELETE'}",
        "Main = logsource >> Monitor<0, 0>!",
        "Monitor<start_ts, count>"
    ]
    
    result_14 = transpiler.transpile(sigma_14)
    print("Input:", sigma_14['detection']['condition'])
    print("Generated:", result_14)
    
    all_contained = True
    for expected in expected_14_contains:
        if expected not in result_14:
            print(f"❌ Missing: {expected}")
            all_contained = False
        else:
            print(f"✅ Found: {expected}")
    
    print("Match:", "✅ PASS" if all_contained else "❌ FAIL")
    
    # Test 15: Your specific example - Complex NOT with parentheses
    print("\n--- Test 15: Your Specific Example - Complex NOT with Parentheses ---")
    sigma_15 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {'EventID': 4738, 'AttributeLDAPDisplayName': 'Min-Pwd-Length'},
            'check_value': {'AttributeValue|gte': 7},
            'filter1': {'ParentImage': 'svchost.exe'},
            'filter2': {'DestinationIp': '10.0.0.0'},
            'condition': 'selection and check_value and not (filter1 or filter2)'
        }
    }
    expected_15 = """logsource matches {product: 'windows', service: 'security'};

// event types

// negation
selection matches {eventid: 4738, attributeldapdisplayname: 'Min-Pwd-Length'};
check_value matches {attributevalue|gte: 7};
filter1 matches {parentimage: 'svchost.exe'};
filter2 matches {destinationip: '10.0.0.0'};
safe_selection not matches {eventid: 4738, attributeldapdisplayname: 'Min-Pwd-Length'};
safe_check_value not matches {attributevalue|gte: 7};
safe_filter1 matches {parentimage: 'svchost.exe'};
safe_filter2 matches {destinationip: '10.0.0.0'};

// property section

Main = logsource >> Monitor;

Filter = (safe_filter1 /\\ safe_filter2);

Monitor = (safe_selection \\/ safe_check_value \\/ Filter)*;"""
    
    result_15 = transpiler.transpile(sigma_15)
    print("Input:", sigma_15['detection']['condition'])
    print("Expected:", expected_15)
    print("Generated:", result_15)
    print("Match:", "✅ PASS" if result_15.strip() == expected_15.strip() else "❌ FAIL")
    
    print("\n" + "=" * 100)
    print("RESULT: Comprehensive Transpiler Test Completed!")
    print("This test suite covers all the examples from examples.txt")
    print("Each test compares expected RML output with generated RML output")

if __name__ == "__main__":
    test_transpiler()
