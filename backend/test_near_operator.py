#!/usr/bin/env python3
"""
Test Near Operator in Temporal Monitor System
Tests the selection1 | near selection2 functionality
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_near_operator():
    """Test the near operator functionality"""
    print("=== Testing Near Operator in Temporal Monitor System ===")
    
    try:
        from app.core.transpiler import SigmaToRMLTranspiler
        
        transpiler = SigmaToRMLTranspiler()
        
        # Test Case 1: Basic near operator
        print("\n--- Test Case 1: Basic near operator ---")
        sigma_rule_1 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    condition: selection1 | near selection2
"""
        
        result_1 = transpiler.transpile(sigma_rule_1)
        print("PASS: Transpilation successful")
        print("Generated RML:")
        print(result_1)
        
        # Test Case 2: Near operator with timeframe
        print("\n--- Test Case 2: Near operator with timeframe ---")
        sigma_rule_2 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    timeframe: 10s
    condition: selection1 | near selection2
"""
        
        result_2 = transpiler.transpile(sigma_rule_2)
        print("PASS: Transpilation successful")
        print("Generated RML:")
        print(result_2)
        
        # Test Case 3: Near operator with complex selections
        print("\n--- Test Case 3: Near operator with complex selections ---")
        sigma_rule_3 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
        Image: 'svchost.exe'
    selection2:
        EventID: 4946
        ServiceName: 'Windows Firewall'
    timeframe: 2m
    condition: selection1 | near selection2
"""
        
        result_3 = transpiler.transpile(sigma_rule_3)
        print("PASS: Transpilation successful")
        print("Generated RML:")
        print(result_3)
        
        print("\nRESULT: Near Operator Test Completed!")
        print("PASS: All test cases transpiled successfully")
        
        # Verify near operator functionality
        print("\nVERIFY: Verifying Near Operator:")
        
        # Check if near operator is detected and handled
        if "| near" in sigma_rule_1 and "Monitor<start_ts, s1, s2>" in result_1:
            print("PASS: Near Operator: Correctly detected and handled")
        else:
            print("FAIL: Near Operator: Not properly detected or handled")
        
        # Check if timeframe is correctly applied
        if "300000" in result_1 and "10000" in result_2 and "120000" in result_3:
            print("PASS: Timeframe: Correctly converted to milliseconds")
        else:
            print("FAIL: Timeframe: Not correctly converted")
        
        # Check if selections are properly defined
        if "safe_selection1" in result_1 and "safe_selection2" in result_1:
            print("PASS: Selections: Properly defined with safe_ prefix")
        else:
            print("FAIL: Selections: Not properly defined")
        
    except Exception as e:
        print(f"FAIL: Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_near_operator()
