#!/usr/bin/env python3
"""
Simple test script to debug transpiler output
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_transpiler():
    """Test the transpiler with a specific case"""
    
    # Test case: not selection_1 or selection_2
    sigma = {
        'logsource': {'product': 'windows', 'service': 'application'},
        'detection': {
            'selection_1': {'EventID': 4728},
            'selection_2': {'objectname': 'test.exe'},
            'condition': 'not selection_1 or selection_2'
        }
    }
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("=== Test Case: not selection_1 or selection_2 ===")
    print("Input Sigma:", sigma['detection']['condition'])
    print("\nGenerated RML:")
    print(result)
    
    # Check if Monitor expression is correct
    if "Monitor = (safe_selection_1 /\\ safe_selection_2)*;" in result:
        print("\n✅ Monitor expression is CORRECT (AND operator)")
    elif "Monitor = (safe_selection_1 \\/ safe_selection_2)*;" in result:
        print("\n❌ Monitor expression is WRONG (OR operator)")
    else:
        print("\n❓ Monitor expression format unclear")

if __name__ == "__main__":
    test_transpiler()
