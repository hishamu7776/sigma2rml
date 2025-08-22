#!/usr/bin/env python3
"""
Debug script for Example 10 specifically
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_example_10():
    """Test Example 10 specifically"""
    
    sigma = {
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
    
    transpiler = RefactoredTranspiler()
    result = transpiler.transpile(sigma)
    
    print("=== Example 10 Debug ===")
    print("Input condition:", sigma['detection']['condition'])
    print("\nGenerated RML:")
    print(result)
    
    # Check specific lines
    lines = result.split('\n')
    for line in lines:
        if 'safe_selection_2' in line:
            print(f"\nFound selection_2 line: {line}")
            if 'not matches' in line:
                print("✅ selection_2 is correctly NOT negated (not matches)")
            elif 'matches' in line and 'not matches' not in line:
                print("❌ selection_2 is incorrectly negated (matches)")

if __name__ == "__main__":
    test_example_10()
