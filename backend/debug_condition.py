#!/usr/bin/env python3
"""
Debug script to see what the condition simplifier is producing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.transpiler_refactored import ConditionSimplifier, QuantifierExpander

def debug_conditions():
    """Debug the condition simplification process"""
    
    # Test case 1: Nested NOT conditions
    condition1 = "selection and not (filter1 or (filter2 and not filter3))"
    print("=== Test Case 1: Nested NOT Conditions ===")
    print(f"Original: {condition1}")
    
    simplifier = ConditionSimplifier()
    simplified1 = simplifier.simplify_condition(condition1)
    print(f"Simplified: {simplified1}")
    print()
    
    # Test case 2: Mixed conditions
    condition2 = "(selection1 or selection2) and not (selection3 and selection4)"
    print("=== Test Case 2: Mixed Conditions ===")
    print(f"Original: {condition2}")
    
    simplified2 = simplifier.simplify_condition(condition2)
    print(f"Simplified: {simplified2}")
    print()
    
    # Test case 3: Quantifier expansion
    condition3 = "all of selection*"
    print("=== Test Case 3: Quantifier Expansion ===")
    print(f"Original: {condition3}")
    
    expander = QuantifierExpander()
    expanded3 = expander.expand_quantifiers(condition3, ['selection1', 'selection2'])
    print(f"Expanded: {expanded3}")
    print()

if __name__ == "__main__":
    debug_conditions()
