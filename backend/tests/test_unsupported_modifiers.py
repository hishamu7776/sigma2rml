#!/usr/bin/env python3
"""
Test unsupported modifiers in Sigma to RML transpiler
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler import SigmaToRMLTranspiler

def test_unsupported_modifiers():
    """Test that unsupported modifiers are properly handled"""
    print("Testing Unsupported Modifiers in Sigma to RML")
    print("=" * 60)
    
    transpiler = SigmaToRMLTranspiler()
    
    # Test 1: Unsupported modifier 'contains'
    print("\n=== Test 1: Unsupported 'contains' modifier ===")
    rule1 = {
        'detection': {
            'selection': {
                'EventID': 4624,
                'CommandLine|contains': 'powershell.exe'
            },
            'condition': 'selection'
        }
    }
    result1 = transpiler.transpile(rule1)
    print(result1)
    
    # Test 2: Unsupported modifier 'startswith'
    print("\n=== Test 2: Unsupported 'startswith' modifier ===")
    rule2 = {
        'detection': {
            'selection': {
                'EventID': 4624,
                'Image|startswith': 'C:\\Windows\\System32'
            },
            'condition': 'selection'
        }
    }
    result2 = transpiler.transpile(rule2)
    print(result2)
    
    # Test 3: Mixed supported and unsupported modifiers
    print("\n=== Test 3: Mixed supported and unsupported modifiers ===")
    rule3 = {
        'detection': {
            'selection': {
                'EventID': 4738,
                'AttributeValue|lte': 7,  # Supported
                'CommandLine|contains': 'admin'  # Unsupported
            },
            'condition': 'selection'
        }
    }
    result3 = transpiler.transpile(rule3)
    print(result3)
    
    # Test 4: Multiple unsupported modifiers
    print("\n=== Test 4: Multiple unsupported modifiers ===")
    rule4 = {
        'detection': {
            'selection': {
                'EventID': 4624,
                'Image|endswith': '.exe',
                'CommandLine|re': '.*admin.*',
                'ProcessName|base64': 'cG93ZXJzaGVsbA=='
            },
            'condition': 'selection'
        }
    }
    result4 = transpiler.transpile(rule4)
    print(result4)
    
    print("\nUnsupported modifiers tests completed!")

if __name__ == "__main__":
    test_unsupported_modifiers()
