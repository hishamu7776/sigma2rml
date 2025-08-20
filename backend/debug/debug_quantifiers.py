#!/usr/bin/env python3
"""
Debug script for quantifier parsing
- all of them
- all of selection*
- 1 of selection*
- N of selection*
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.ast.condition_parser import ConditionParser

def debug_quantifier_parsing():
    """Debug quantifier parsing specifically"""
    
    test_cases = [
        ("all of them", ["selection_1", "selection_2"]),
        ("all of selection*", ["selection_base", "selection_eventValue"]),
        ("1 of selection*", ["selection_base", "selection_eventValue"]),
        ("2 of selection*", ["selection_base", "selection_eventValue", "selection_extra"]),
        ("any of them", ["selection_1", "selection_2"])
    ]
    
    for condition_str, available_names in test_cases:
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
        print("\nTokenization:")
        tokens = parser.tokenize(condition_str)
        print(f"Tokens: {tokens}")
        
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    print("🔍 Debugging Quantifier Parsing")
    print("=" * 60)
    debug_quantifier_parsing()
