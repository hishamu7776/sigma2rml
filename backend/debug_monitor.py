#!/usr/bin/env python3
"""
Debug script to test monitor expression generation
"""

from typing import List

def test_monitor_generation():
    """Test the monitor expression generation logic"""
    
    def generate_monitor_expression(condition: str, selections: List[str]) -> str:
        """Generate the monitor expression based on the actual condition structure"""
        safe_selections = [f"safe_{s}" for s in selections]
        
        # Check for unsupported patterns first
        if 'UNSUPPORTED_' in condition:
            return f"Monitor = UNSUPPORTED_PATTERN; // {condition}"
        
        # Check if the condition contains the expanded quantifier
        if 'selection1 and selection2' in condition and len(selections) == 2:
            # This is likely a "2 of selection*" case
            return f"Monitor = UNSUPPORTED_PATTERN; // 2 of selection* not supported"
        
        # Analyze the original condition structure more carefully
        # For single selection, just use the selection directly
        if len(selections) == 1:
            return f"Monitor = {safe_selections[0]}*;"
        
        # For multiple selections, we need to determine the logical operator
        # Look at the original condition before expansion
        original_condition = condition
        
        print(f"DEBUG: Analyzing condition: '{original_condition}'")
        print(f"DEBUG: Contains ' and ': {' and ' in original_condition}")
        print(f"DEBUG: Contains ' or ': {' or ' in original_condition}")
        
        # Check for quantifier patterns
        if 'any of selection*' in original_condition:
            return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
        elif 'all of selection*' in original_condition:
            return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        elif '1 of selection*' in original_condition:
            return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
        elif '2 of selection*' in original_condition or '3 of selection*' in original_condition:
            return f"Monitor = UNSUPPORTED_PATTERN; // {original_condition} not supported"
        
        # Check for explicit AND/OR patterns in the original condition
        if ' and ' in original_condition:
            print(f"DEBUG: Using AND operator")
            return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        elif ' or ' in original_condition:
            print(f"DEBUG: Using OR operator")
            return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
        
        # Default case: assume AND for multiple selections
        print(f"DEBUG: Using default AND operator")
        return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
    
    # Test cases
    test_cases = [
        ("not selection_1 or selection_2", ["selection_1", "selection_2"]),
        ("selection1 and (selection2 or selection3)", ["selection1", "selection2", "selection3"]),
        ("all of selection*", ["selection1", "selection2"]),
    ]
    
    for condition, selections in test_cases:
        print(f"\n=== Testing: {condition} ===")
        result = generate_monitor_expression(condition, selections)
        print(f"Result: {result}")

if __name__ == "__main__":
    test_monitor_generation()
