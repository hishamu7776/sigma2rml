#!/usr/bin/env python3
"""
Test temporal operators in Sigma to RML
- selection1 | near selection2 (with and without timeframe)
- selection1 and selection2 with timeframe
- selection1 and selection2 and selection3 with timeframe
- all of selection* with timeframe
- selection | count() > N
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler import SigmaToRMLTranspiler

def test_near_without_timeframe():
    """Test 'selection1 | near selection2' without timeframe (default 10s)"""
    print("=== Near Without Timeframe Test (Default 10s) ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection_priv_add': {
                'EventID': 4728
            },
            'selection_log_clear': {
                'EventID': 1102
            },
            'condition': 'selection_priv_add | near selection_log_clear'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_near_with_timeframe():
    """Test 'selection1 | near selection2' with explicit timeframe"""
    print("=== Near With Timeframe Test (5m) ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection_priv_add': {
                'EventID': 4728
            },
            'selection_log_clear': {
                'EventID': 1102
            },
            'timeframe': '5m',
            'condition': 'selection_priv_add | near selection_log_clear'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_and_with_timeframe():
    """Test 'selection1 and selection2' with timeframe"""
    print("=== AND With Timeframe Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection_task': {
                'EventID': 4698
            },
            'selection_firewall': {
                'EventID': 4946
            },
            'timeframe': '5m',
            'condition': 'selection_task and selection_firewall'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_three_way_and_with_timeframe():
    """Test 'selection1 and selection2 and selection3' with timeframe"""
    print("=== Three-Way AND With Timeframe Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection_task': {
                'EventID': 4698
            },
            'selection_firewall': {
                'EventID': 4946
            },
            'selection_login': {
                'EventID': 4624
            },
            'timeframe': '2m',
            'condition': 'selection_task and selection_firewall and selection_login'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_all_of_selection_star_with_timeframe():
    """Test 'all of selection*' with timeframe"""
    print("=== All of Selection* With Timeframe Test ===")
    
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
            'timeframe': '1m',
            'condition': 'all of selection*'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

def test_count_operator():
    """Test 'selection | count() > N' pattern"""
    print("=== Count Operator Test ===")
    
    sigma_rule = {
        'logsource': {
            'product': 'windows',
            'service': 'security'
        },
        'detection': {
            'selection': {
                'EventID': 4663,
                'Accesses': 'DELETE'
            },
            'timeframe': '1m',
            'condition': 'selection | count() > 5'
        }
    }
    
    transpiler = SigmaToRMLTranspiler()
    result = transpiler.transpile(sigma_rule)
    print(result)
    print()

if __name__ == "__main__":
    print("Testing Temporal Operators in Sigma to RML")
    print("=" * 50)
    
    test_near_without_timeframe()
    test_near_with_timeframe()
    test_and_with_timeframe()
    test_three_way_and_with_timeframe()
    test_all_of_selection_star_with_timeframe()
    test_count_operator()
    
    print("Temporal operator tests completed!")
