#!/usr/bin/env python3
"""
Test the new modifier approach in Sigma to RML transpiler
Tests modifiers directly in selection with multiple fields
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler import SigmaToRMLTranspiler

def test_new_modifier_approach():
    """Test the new modifier approach with modifiers directly in selection"""
    print("Testing New Modifier Approach in Sigma to RML")
    print("=" * 60)
    
    transpiler = SigmaToRMLTranspiler()
    
    # Test 1: Single field with modifier (as shown in the use case)
    print("\n=== Test 1: Single field with modifier ===")
    rule1 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length',
                'AttributeValue|gte': 7
            },
            'condition': 'selection'
        }
    }
    result1 = transpiler.transpile(rule1)
    print(result1)
    
    # Test 2: Multiple fields with modifiers (as shown in the use case)
    print("\n=== Test 2: Multiple fields with modifiers ===")
    rule2 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length',
                'AttributeValue|gte': 7,
                'AttributeNumber|gt': 10
            },
            'condition': 'selection'
        }
    }
    result2 = transpiler.transpile(rule2)
    print(result2)
    
    # Test 3: Mixed modifiers and regular fields
    print("\n=== Test 3: Mixed modifiers and regular fields ===")
    rule3 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length',
                'AttributeValue|gte': 7,
                'AttributeNumber|gt': 10,
                'Status': 'Success'
            },
            'condition': 'selection'
        }
    }
    result3 = transpiler.transpile(rule3)
    print(result3)
    
    # Test 4: Different comparison operators
    print("\n=== Test 4: Different comparison operators ===")
    rule4 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length',
                'AttributeValue|gte': 7,
                'AttributeNumber|gt': 10,
                'AttributeCount|lt': 100,
                'AttributeSize|lte': 1024
            },
            'condition': 'selection'
        }
    }
    result4 = transpiler.transpile(rule4)
    print(result4)
    
    # Test 5: Complex condition with multiple selections
    print("\n=== Test 5: Complex condition with multiple selections ===")
    rule5 = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection1': {
                'EventID': 4738,
                'AttributeLDAPDisplayName': 'Min-Pwd-Length',
                'AttributeValue|gte': 7
            },
            'selection2': {
                'EventID': 4739,
                'AttributeLDAPDisplayName': 'Max-Pwd-Age',
                'AttributeValue|lt': 90
            },
            'condition': 'selection1 and selection2'
        }
    }
    result5 = transpiler.transpile(rule5)
    print(result5)
    
    print("\nNew modifier approach tests completed!")

if __name__ == "__main__":
    test_new_modifier_approach()
