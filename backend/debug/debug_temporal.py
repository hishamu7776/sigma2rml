#!/usr/bin/env python3
"""
Debug script for temporal operator parsing
- selection1 | near selection2
- selection1 | near selection2 with timeframe
- selection1 and selection2 with timeframe
- selection | count() > N
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.ast.condition_parser import ConditionParser

def debug_temporal_parsing():
    """Debug temporal operator parsing specifically"""
    
    test_cases = [
        ("selection1 | near selection2", ["selection1", "selection2"]),
        ("selection_priv_add | near selection_log_clear", ["selection_priv_add", "selection_log_clear"]),
        ("selection1 and selection2", ["selection1", "selection2"]),
        ("selection1 and selection2 and selection3", ["selection1", "selection2", "selection3"]),
        ("all of selection*", ["selection_base", "selection_eventValue"]),
        ("1 of selection*", ["selection_base", "selection_eventValue"])
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

def debug_count_operator():
    """Debug count operator specifically"""
    print("🔍 Debugging Count Operator")
    print("=" * 60)
    
    condition_str = "selection | count() > 5"
    available_names = ["selection"]
    
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

if __name__ == "__main__":
    print("🔍 Debugging Temporal Operator Parsing")
    print("=" * 60)
    debug_temporal_parsing()
    debug_count_operator()
