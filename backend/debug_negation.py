#!/usr/bin/env python3
"""
Debug script to test negation detection logic
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app', 'core'))

from transpiler_refactored import ConditionSimplifier

def test_negation_detection():
    print("=== Testing Negation Detection ===\n")
    
    # Test case 1: Nested NOT Conditions
    condition1 = "selection and not filter1 and (not filter2 or filter3)"
    print(f"Condition 1: {condition1}")
    print(f"filter1 negated: {ConditionSimplifier._is_selection_negated('filter1', condition1)}")
    print(f"filter2 negated: {ConditionSimplifier._is_selection_negated('filter2', condition1)}")
    print(f"filter3 negated: {ConditionSimplifier._is_selection_negated('filter3', condition1)}")
    print()
    
    # Test case 2: Mixed Conditions
    condition2 = "(selection1 or selection2) and (not selection3 or not selection4)"
    print(f"Condition 2: {condition2}")
    print(f"selection3 negated: {ConditionSimplifier._is_selection_negated('selection3', condition2)}")
    print(f"selection4 negated: {ConditionSimplifier._is_selection_negated('selection4', condition2)}")
    print()
    
    # Test the regex pattern
    import re
    paren_pattern = r'not\s*\(([^)]+)\)'
    print("=== Testing Regex Pattern ===")
    print(f"Pattern: {paren_pattern}")
    
    # Test with condition1
    matches1 = re.findall(paren_pattern, condition1)
    print(f"Condition 1 matches: {matches1}")
    
    # Test with condition2
    matches2 = re.findall(paren_pattern, condition2)
    print(f"Condition 2 matches: {matches2}")
    
    # Test the additional pattern
    paren_pattern2 = r'\(([^)]+)\)'
    print(f"\n=== Testing Additional Pattern ===")
    print(f"Pattern: {paren_pattern2}")
    
    # Test with condition1
    paren_matches1 = re.findall(paren_pattern2, condition1)
    print(f"Condition 1 paren matches: {paren_matches1}")
    
    # Test with condition2
    paren_matches2 = re.findall(paren_pattern2, condition2)
    print(f"Condition 2 paren matches: {paren_matches2}")
    
    # Test specific cases
    print(f"\n=== Testing Specific Cases ===")
    print(f"filter2 in '(not filter2 or filter3)': {'filter2' in '(not filter2 or filter3)'}")
    print(f"'not filter2' in '(not filter2 or filter3)': {'not filter2' in '(not filter2 or filter3)'}")
    print(f"selection4 in '(not selection3 or not selection4)': {'selection4' in '(not selection3 or not selection4)'}")
    print(f"'not selection4' in '(not selection3 or not selection4)': {'not selection4' in '(not selection3 or not selection4)'}")

if __name__ == "__main__":
    test_negation_detection()
