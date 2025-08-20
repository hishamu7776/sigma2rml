#!/usr/bin/env python3
"""
Debug script for temporal operators
"""

from app.core.ast.condition_parser import ConditionParser

def debug_temporal():
    # Create a mock available_names
    available_names = {
        'selection1': 'selection1',
        'selection2': 'selection2'
    }
    
    parser = ConditionParser(available_names)
    
    # Test the temporal parsing directly
    condition = "selection1 | near selection2"
    print(f"Testing condition: {condition}")
    
    # Tokenize
    tokens = parser.tokenize(condition)
    print(f"Tokens: {tokens}")
    
    # Parse
    result = parser.parse(condition)
    print(f"Result: {result}")
    print(f"RML: {result.to_rml()}")

if __name__ == "__main__":
    debug_temporal()
