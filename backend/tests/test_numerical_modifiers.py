#!/usr/bin/env python3
"""
Test numerical modifiers in Sigma to RML transpiler
Tests various comparison operators and NOT conditions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_numerical_modifiers():
    """Test numerical modifiers with different operators and conditions"""
    print("Testing Numerical Modifiers in Sigma to RML")
    print("=" * 60)
    
    transpiler = RefactoredTranspiler()
    
    # Test 1: gte (greater than or equal) operator
    print("\n=== Test 1: gte (>=) operator ===")
    rule1 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'check_value': {
                'AttributeValue|gte': 7
            },
            'condition': 'selection and check_value'
        }
    }
    result1 = transpiler.transpile(rule1)
    print(result1)
    
    # Test 2: gt (greater than) operator
    print("\n=== Test 2: gt (>) operator ===")
    rule2 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'check_value': {
                'AttributeValue|gt': 7
            },
            'condition': 'selection and check_value'
        }
    }
    result2 = transpiler.transpile(rule2)
    print(result2)
    
    # Test 3: Invalid operator (typo: 'te' instead of 'gte')
    print("\n=== Test 3: Invalid operator 'te' (should be marked as unsupported) ===")
    rule3 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'check_value': {
                'AttributeValue|te': 7
            },
            'condition': 'selection and check_value'
        }
    }
    result3 = transpiler.transpile(rule3)
    print(result3)
    
    # Test 4: gte with NOT condition
    print("\n=== Test 4: gte (>=) operator with NOT condition ===")
    rule4 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'check_value': {
                'AttributeValue|gte': 7
            },
            'condition': 'selection and not check_value'
        }
    }
    result4 = transpiler.transpile(rule4)
    print(result4)
    
    # Test 5: gt with NOT condition
    print("\n=== Test 5: gt (>) operator with NOT condition ===")
    rule5 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'check_value': {
                'AttributeValue|gt': 7
            },
            'condition': 'selection and not check_value'
        }
    }
    result5 = transpiler.transpile(rule5)
    print(result5)
    
    # Test 6: Invalid operator with NOT condition
    print("\n=== Test 6: Invalid operator 'te' with NOT condition ===")
    rule6 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'check_value': {
                'AttributeValue|te': 7
            },
            'condition': 'selection and not check_value'
        }
    }
    result6 = transpiler.transpile(rule6)
    print(result6)
    
    # Test 7: Mixed valid and invalid operators
    print("\n=== Test 7: Mixed valid and invalid operators ===")
    rule7 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length'
            },
            'check_value': {
                'AttributeValue|gte': 7
            },
            'invalid_check': {
                'AttributeValue|te': 5
            },
            'condition': 'selection and check_value and invalid_check'
        }
    }
    result7 = transpiler.transpile(rule7)
    print(result7)
    
    print("\nNumerical modifiers tests completed!")

if __name__ == "__main__":
    test_numerical_modifiers()
