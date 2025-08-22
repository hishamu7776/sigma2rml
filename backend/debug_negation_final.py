#!/usr/bin/env python3
"""
Debug script to test negation detection for the failing case
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.transpiler_refactored import ConditionSimplifier

def test_negation_detection():
    """Test negation detection for the specific failing case"""
    
    condition = "not selection_1 or selection_2"
    
    print(f"=== Testing negation detection for: '{condition}' ===")
    
    # Test each selection
    selections = ["selection_1", "selection_2"]
    
    for selection in selections:
        is_negated = ConditionSimplifier._is_selection_negated(selection, condition)
        print(f"{selection}: is_negated = {is_negated}")
    
    print("\nExpected results:")
    print("selection_1: is_negated = True  (because 'not selection_1')")
    print("selection_2: is_negated = False (because just 'selection_2')")

if __name__ == "__main__":
    test_negation_detection()
