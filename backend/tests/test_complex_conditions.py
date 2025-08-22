#!/usr/bin/env python3
"""
Test complex conditions in Sigma to RML
- Complex nested conditions with not
- Multiple filters with complex logic
- Edge cases and error handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_complex_not_condition():
    """Test complex condition with NOT and parentheses"""
    print("=== Complex NOT Condition Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'edr'
        },
        'detection': {
            'selection': {
                'Image': 'werfault.exe'
            },
            'filter1': {
                'ParentImage': 'svchost.exe'
            },
            'filter2': {
                'DestinationIp': [
                    '10.0.0.0',
                    '172.16.0.0',
                    '192.168.0.0'
                ]
            },
            'filter3': {
                'DestinationHostname': [
                    'windowsupdate.com',
                    'microsoft.com'
                ]
            },
            'condition': 'selection and not (filter1 or filter2 or filter3)'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_comparison_operators():
    """Test comparison operators like lte, gte, etc."""
    print("=== Comparison Operators Test ===")
    
    sigma_rule = {
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
                'AttributeValue|lte': 7
            },
            'condition': 'selection and check_value'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_multiple_filters():
    """Test multiple filters with complex logic"""
    print("=== Multiple Filters Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4663,
                'Accesses|all': [
                    'ReadData',
                    'WriteData',
                    'DELETE'
                ]
            },
            'condition': 'selection'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_empty_condition():
    """Test handling of empty condition"""
    print("=== Empty Condition Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4624
            },
            'condition': ''
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_invalid_yaml():
    """Test handling of invalid YAML"""
    print("=== Invalid YAML Test ===")
    
    try:
        # This should be handled gracefully
        transpiler = RefactoredTranspiler()
        result = transpiler.transpile("invalid yaml content")
        print(result)
    except Exception as e:
        print(f"Expected error caught: {e}")
    print()

if __name__ == "__main__":
    print("Testing Complex Conditions in Sigma to RML")
    print("=" * 50)
    
    test_complex_not_condition()
    test_comparison_operators()
    test_multiple_filters()
    test_empty_condition()
    test_invalid_yaml()
    
    print("Complex condition tests completed!")
