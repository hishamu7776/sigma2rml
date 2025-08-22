#!/usr/bin/env python3
"""
Script to fix all remaining SigmaToRMLTranspiler references in test files
"""

import os

def fix_examples_file():
    """Fix all SigmaToRMLTranspiler references in the examples test file"""
    file_path = 'tests/examples/test_examples_exact.py'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace all remaining instances
    content = content.replace('transpiler = SigmaToRMLTranspiler()', 'transpiler = RefactoredTranspiler()')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_examples_file()
