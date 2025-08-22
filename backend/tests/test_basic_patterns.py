#!/usr/bin/env python3
"""
Test basic Sigma to RML patterns
- Simple selections
- Multiple EventIDs
- Basic logical operators (and, or, not)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_simple_selection():
    """Test simple selection pattern"""
    print("=== Simple Selection Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'application'
        },
        'detection': {
            'selection': {
                'EventID': 524,
                'Provider_Name': 'Microsoft-Windows-Backup'
            },
            'condition': 'selection'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_multiple_eventids():
    """Test multiple EventIDs pattern"""
    print("=== Multiple EventIDs Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': [4728, 4729, 4730]
            },
            'condition': 'selection'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_basic_logical_operators():
    """Test basic logical operators"""
    print("=== Basic Logical Operators Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection_1': {
                'EventID': 4663
            },
            'selection_2': {
                'ObjectName': '\\Device\\CdRom0\\setup.exe'
            },
            'condition': 'selection_1 and selection_2'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_or_condition():
    """Test OR condition pattern"""
    print("=== OR Condition Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'aws',
            'service': 'cloudtrail'
        },
        'detection': {
            'selection1': {
                'eventSource': 'sts.amazonaws.com',
                'eventName': 'AssumeRoleWithSAML'
            },
            'selection2': {
                'eventSource': 'iam.amazonaws.com',
                'eventName': 'UpdateSAMLProvider'
            },
            'condition': 'selection1 or selection2'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

if __name__ == "__main__":
    print("Testing Basic Sigma to RML Patterns")
    print("=" * 50)
    
    test_simple_selection()
    test_multiple_eventids()
    test_basic_logical_operators()
    test_or_condition()
    
    print("Basic pattern tests completed!")
