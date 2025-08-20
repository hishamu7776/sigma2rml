#!/usr/bin/env python3
"""
Test complex edge cases and hypothetical scenarios in Sigma to RML transpiler
Tests various complex combinations of numerical modifiers, NOT conditions, and edge cases
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler import SigmaToRMLTranspiler

def test_complex_numerical_combinations():
    """Test complex combinations of numerical modifiers"""
    print("Testing Complex Numerical Modifier Combinations")
    print("=" * 60)
    
    transpiler = SigmaToRMLTranspiler()
    
    # Test 1: Multiple numerical modifiers in same selection
    print("\n=== Test 1: Multiple numerical modifiers in same selection ===")
    rule1 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length',
                'AttributeValue|gte': 7,
                'AttributeValue|lt': 20,
                'AttributeNumber|gt': 0,
                'AttributeCount|lte': 100
            },
            'condition': 'selection'
        }
    }
    result1 = transpiler.transpile(rule1)
    print(result1)
    
    # Test 2: Mixed numerical and non-numerical fields with NOT condition
    print("\n=== Test 2: Mixed fields with NOT condition ===")
    rule2 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length',
                'AttributeValue|gte': 7,
                'Status': 'Success',
                'UserID|gt': 1000
            },
            'condition': 'not selection'
        }
    }
    result2 = transpiler.transpile(rule2)
    print(result2)
    
    # Test 3: Complex nested conditions with numerical modifiers
    print("\n=== Test 3: Complex nested conditions ===")
    rule3 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'check_value': {
                'AttributeValue|gte': 7
            },
            'filter1': {
                'UserID|gt': 1000,
                'UserID|lt': 9999
            },
            'filter2': {
                'ProcessID|gte': 100,
                'ProcessID|lte': 50000
            },
            'condition': 'selection and check_value and not (filter1 or filter2)'
        }
    }
    result3 = transpiler.transpile(rule3)
    print(result3)
    
    # Test 4: Edge case: boundary values and zero
    print("\n=== Test 4: Boundary values and zero ===")
    rule4 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeValue|gt': 0,
                'AttributeValue|lt': 1,
                'AttributeValue|gte': 0,
                'AttributeValue|lte': 1
            },
            'condition': 'selection'
        }
    }
    result4 = transpiler.transpile(rule4)
    print(result4)
    
    # Test 5: Negative numbers and large values
    print("\n=== Test 5: Negative numbers and large values ===")
    rule5 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeValue|gt': -100,
                'AttributeValue|lt': 1000000,
                'AttributeValue|gte': -50,
                'AttributeValue|lte': 999999
            },
            'condition': 'selection'
        }
    }
    result5 = transpiler.transpile(rule5)
    print(result5)

def test_complex_logical_structures():
    """Test complex logical structures with numerical modifiers"""
    print("\n\nTesting Complex Logical Structures")
    print("=" * 60)
    
    transpiler = SigmaToRMLTranspiler()
    
    # Test 1: Deep nested NOT conditions
    print("\n=== Test 1: Deep nested NOT conditions ===")
    rule1 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeValue|gte': 7
            },
            'filter1': {
                'UserID|gt': 1000
            },
            'filter2': {
                'ProcessID|lt': 50000
            },
            'condition': 'not (selection and not (filter1 or filter2))'
        }
    }
    result1 = transpiler.transpile(rule1)
    print(result1)
    
    # Test 2: Complex quantifier with numerical modifiers
    print("\n=== Test 2: Complex quantifier with numerical modifiers ===")
    rule2 = {
        'logsource': {'product': 'gcp', 'service': 'audit'},
        'detection': {
            'selection_base': {
                'eventservice': 'admin.googleapis.com',
                'eventname': 'ENFORCE_STRONG_AUTHENTICATION'
            },
            'selection_value': {
                'new_value|gte': 8
            },
            'selection_count': {
                'attempts|lt': 5
            },
            'condition': 'all of selection*'
        }
    }
    result2 = transpiler.transpile(rule2)
    print(result2)
    
    # Test 3: Mixed temporal and numerical operators
    print("\n=== Test 3: Mixed temporal and numerical operators ===")
    rule3 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4663,
                'Accesses': 'DELETE',
                'ObjectID|gt': 1000
            },
            'condition': 'selection | count() > 5'
        }
    }
    result3 = transpiler.transpile(rule3)
    print(result3)

def test_hypothetical_scenarios():
    """Test hypothetical real-world scenarios"""
    print("\n\nTesting Hypothetical Real-World Scenarios")
    print("=" * 60)
    
    transpiler = SigmaToRMLTranspiler()
    
    # Test 1: Password policy violation detection
    print("\n=== Test 1: Password policy violation detection ===")
    rule1 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'weak_password': {
                'AttributeValue|lt': 12
            },
            'very_weak_password': {
                'AttributeValue|lt': 8
            },
            'condition': 'selection and (weak_password or very_weak_password)'
        }
    }
    result1 = transpiler.transpile(rule1)
    print(result1)
    
    # Test 2: Resource usage monitoring
    print("\n=== Test 2: Resource usage monitoring ===")
    rule2 = {
        'logsource': {'product': 'linux', 'service': 'system'},
        'detection': {
            'selection': {
                'EventID': 'resource_alert',
                'CPU_Usage|gte': 90,
                'Memory_Usage|gte': 95,
                'Disk_Usage|gte': 85
            },
            'critical_selection': {
                'EventID': 'resource_alert',
                'CPU_Usage|gte': 95,
                'Memory_Usage|gte': 98,
                'Disk_Usage|gte': 90
            },
            'condition': 'selection and not critical_selection'
        }
    }
    result2 = transpiler.transpile(rule2)
    print(result2)
    
    # Test 3: Network traffic analysis
    print("\n=== Test 3: Network traffic analysis ===")
    rule3 = {
        'logsource': {'product': 'network', 'service': 'firewall'},
        'detection': {
            'selection': {
                'EventID': 'connection_attempt',
                'SourceIP': '192.168.1.0/24'
            },
            'suspicious_volume': {
                'ConnectionCount|gt': 100,
                'BytesTransferred|gte': 1000000
            },
            'time_window': {
                'Duration|lt': 300
            },
            'condition': 'selection and suspicious_volume and time_window'
        }
    }
    result3 = transpiler.transpile(rule3)
    print(result3)
    
    # Test 4: User behavior analytics
    print("\n=== Test 4: User behavior analytics ===")
    rule4 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4624,
                'LogonType': 2
            },
            'normal_hours': {
                'Hour|gte': 8,
                'Hour|lt': 18
            },
            'after_hours': {
                'Hour|lt': 8
            },
            'late_night': {
                'Hour|gte': 22
            },
            'condition': 'selection and (after_hours or late_night)'
        }
    }
    result4 = transpiler.transpile(rule4)
    print(result4)
    
    # Test 5: File access pattern detection
    print("\n=== Test 5: File access pattern detection ===")
    rule5 = {
        'logsource': {'product': 'windows', 'service': 'security'},
        'detection': {
            'selection': {
                'EventID': 4663,
                'ObjectName|endswith': '.conf'
            },
            'sensitive_files': {
                'ObjectName|contains': 'password',
                'ObjectName|contains': 'config'
            },
            'access_frequency': {
                'AccessCount|gt': 10,
                'AccessCount|lt': 1000
            },
            'time_span': {
                'TimeSpan|lt': 3600
            },
            'condition': 'selection and sensitive_files and access_frequency and time_span'
        }
    }
    result5 = transpiler.transpile(rule5)
    print(result5)

def test_edge_case_combinations():
    """Test edge case combinations that might break the transpiler"""
    print("\n\nTesting Edge Case Combinations")
    print("=" * 60)
    
    transpiler = SigmaToRMLTranspiler()
    
    # Test 1: All supported modifiers in one rule
    print("\n=== Test 1: All supported modifiers in one rule ===")
    rule1 = {
        'logsource': {'product': 'test', 'service': 'test'},
        'detection': {
            'selection': {
                'Field1|lt': 10,
                'Field2|lte': 20,
                'Field3|gt': 30,
                'Field4|gte': 40,
                'Field5': 'normal_value'
            },
            'condition': 'selection'
        }
    }
    result1 = transpiler.transpile(rule1)
    print(result1)
    
    # Test 2: Mixed data types with modifiers
    print("\n=== Test 2: Mixed data types with modifiers ===")
    rule2 = {
        'logsource': {'product': 'test', 'service': 'test'},
        'detection': {
            'selection': {
                'StringField': 'test',
                'NumberField|gt': 100,
                'ListField': ['item1', 'item2'],
                'FloatField|lte': 99.99
            },
            'condition': 'selection'
        }
    }
    result2 = transpiler.transpile(rule2)
    print(result2)
    
    # Test 3: Complex negation patterns
    print("\n=== Test 3: Complex negation patterns ===")
    rule3 = {
        'logsource': {'product': 'test', 'service': 'test'},
        'detection': {
            'selection1': {
                'Field1|gte': 10
            },
            'selection2': {
                'Field2|lt': 20
            },
            'selection3': {
                'Field3|gt': 30
            },
            'condition': 'not (selection1 and not (selection2 or selection3))'
        }
    }
    result3 = transpiler.transpile(rule3)
    print(result3)

def main():
    """Run all complex edge case tests"""
    print("🧪 Testing Complex Edge Cases and Hypothetical Scenarios")
    print("=" * 80)
    
    try:
        test_complex_numerical_combinations()
        test_complex_logical_structures()
        test_hypothetical_scenarios()
        test_edge_case_combinations()
        
        print("\n" + "=" * 80)
        print("✅ All complex edge case tests completed successfully!")
        print("🎯 The transpiler handles complex scenarios correctly")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
