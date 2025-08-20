#!/usr/bin/env python3
"""
Debug script for quantifier parsing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.ast.condition_parser import ConditionParser

def debug_quantifier_parsing():
    """Debug the quantifier parsing logic"""
    
    # Test the "1 of selection*" pattern
    condition_str = "1 of selection*"
    available_names = ["selection_base", "selection_eventValue"]
    
    print(f"Testing condition: '{condition_str}'")
    print(f"Available names: {available_names}")
    print("-" * 50)
    
    # Create parser and parse
    parser = ConditionParser(available_names)
    result = parser.parse(condition_str)
    
    print(f"Parse result: {result}")
    print(f"Result type: {type(result)}")
    print(f"Result.to_rml(): {result.to_rml()}")
    
    # Also test tokenization
    print("\n" + "=" * 50)
    print("Tokenization debug:")
    tokens = parser.tokenize(condition_str)
    print(f"Tokens: {tokens}")
    
    # Test individual patterns
    print("\n" + "=" * 50)
    print("Pattern matching debug:")
    
    import re
    patterns = [
        r'1 of',
        r'selection\*',
        r'\w+\*'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, condition_str)
        print(f"Pattern '{pattern}': {matches}")

if __name__ == "__main__":
    debug_quantifier_parsing()
