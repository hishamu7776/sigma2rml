#!/usr/bin/env python3
"""
Test quantifier patterns in Sigma to RML
- all of them
- all of selection*
- 1 of selection*
- N of selection*
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler import SigmaToRMLTranspiler

def test_all_of_them():
    """Test 'all of them' pattern"""
    print("=== All of Them Test ===")
    
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
            'condition': 'all of them'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_all_of_selection_star():
    """Test 'all of selection*' pattern"""
    print("=== All of Selection* Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'gcp',
            'service': 'audit'
        },
        'detection': {
            'selection_base': {
                'eventService': 'admin.googleapis.com',
                'eventName': [
                    'ENFORCE_STRONG_AUTHENTICATION',
                    'ALLOW_STRONG_AUTHENTICATION'
                ]
            },
            'selection_eventValue': {
                'new_value': 'false'
            },
            'condition': 'all of selection*'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_1_of_selection_star():
    """Test '1 of selection*' pattern"""
    print("=== 1 of Selection* Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'gcp',
            'service': 'audit'
        },
        'detection': {
            'selection_base': {
                'eventService': 'admin.googleapis.com',
                'eventName': [
                    'ENFORCE_STRONG_AUTHENTICATION',
                    'ALLOW_STRONG_AUTHENTICATION'
                ]
            },
            'selection_eventValue': {
                'new_value': 'false'
            },
            'condition': '1 of selection*'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_n_of_selection_star():
    """Test 'N of selection*' pattern where N > 1"""
    print("=== N of Selection* Test (N > 1) ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'gcp',
            'service': 'audit'
        },
        'detection': {
            'selection_base': {
                'eventService': 'admin.googleapis.com',
                'eventName': [
                    'ENFORCE_STRONG_AUTHENTICATION',
                    'ALLOW_STRONG_AUTHENTICATION'
                ]
            },
            'selection_eventValue': {
                'new_value': 'false'
            },
            'selection_extra': {
                'eventType': 'admin'
            },
            'condition': '2 of selection*'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

if __name__ == "__main__":
    print("Testing Quantifier Patterns in Sigma to RML")
    print("=" * 50)
    
    test_all_of_them()
    test_all_of_selection_star()
    test_1_of_selection_star()
    test_n_of_selection_star()
    
    print("Quantifier pattern tests completed!")
