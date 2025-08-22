#!/usr/bin/env python3
"""
Debug script to see the expanded condition
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.transpiler_refactored import RefactoredTranspiler, ConditionSimplifier

def test_condition_processing():
    """Test condition processing steps"""
    
    original_condition = "not selection_1 or selection_2"
    selections = ["selection_1", "selection_2"]
    
    print("=== Condition Processing Debug ===")
    print(f"Original condition: '{original_condition}'")
    
    # Step 1: Simplify condition
    condition_simplifier = ConditionSimplifier()
    simplified_condition = condition_simplifier.simplify_condition(original_condition)
    print(f"Simplified condition: '{simplified_condition}'")
    
    # Step 2: Test negation detection on simplified condition
    for selection in selections:
        is_negated = ConditionSimplifier._is_selection_negated(selection, simplified_condition)
        print(f"{selection}: is_negated = {is_negated} (from simplified condition)")

if __name__ == "__main__":
    test_condition_processing()
