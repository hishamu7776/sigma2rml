#!/usr/bin/env python3
"""
Script to replace Unicode characters in test files with ASCII equivalents
"""

import os
import re

def fix_unicode_in_file(filepath):
    """Replace Unicode characters in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace Unicode characters with ASCII equivalents
        replacements = {
            '✅': 'PASS',
            '❌': 'FAIL',
            '🧪': 'TEST',
            '🔍': 'VERIFY',
            '📋': 'RUNNING',
            '📊': 'SUMMARY',
            '🎯': 'RESULT',
            '⚠️': 'WARNING',
            '🔧': 'RECOMMEND',
            '📁': 'CATEGORY',
            '🎉': 'SUCCESS',
            '\U0001f9ea': 'TEST'  # Test tube emoji
        }
        
        for unicode_char, ascii_text in replacements.items():
            content = content.replace(unicode_char, ascii_text)
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {filepath}")
        return True
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all test files"""
    test_files = [
        'test_enhanced_temporal.py',
        'test_fixed_temporal.py',
        'test_near_operator.py',
        'test_apis.py',
        'test_improved_apis.py',
        'test_rml_endpoint.py',
        'test_path_fix.py',
        'test_final_validation.py'
    ]
    
    print("Fixing Unicode characters in test files...")
    
    for test_file in test_files:
        if os.path.exists(test_file):
            fix_unicode_in_file(test_file)
        else:
            print(f"File not found: {test_file}")
    
    print("Unicode fix complete!")

if __name__ == "__main__":
    main()
