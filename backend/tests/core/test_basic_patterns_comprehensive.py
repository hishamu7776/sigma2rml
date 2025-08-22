#!/usr/bin/env python3
"""
Comprehensive Test for Basic Pattern Matching
Tests that basic patterns like selection1 and selection2, any of selection*, etc. still work
after implementing the enhanced temporal monitor system
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_basic_and_conditions():
    """Test basic AND conditions"""
    print("=== Testing Basic AND Conditions ===")
    
    try:
        from app.core.transpiler_refactored import RefactoredTranspiler
        
        transpiler = RefactoredTranspiler()
        
        # Test Case 1: Simple AND
        print("\n--- Test Case 1: selection1 and selection2 ---")
        sigma_rule_1 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    condition: selection1 and selection2
"""
        
        result_1 = transpiler.transpile(sigma_rule_1)
        print("Generated RML:")
        print(result_1)
        
        # Verify it's NOT using temporal monitor
        if "Monitor<start_ts" in result_1:
            print("FAIL: Basic AND condition incorrectly using temporal monitor")
        else:
            print("PASS: Basic AND condition correctly handled without temporal monitor")
        
        # Test Case 2: Three selections with AND
        print("\n--- Test Case 2: selection1 and selection2 and selection3 ---")
        sigma_rule_2 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    selection3:
        EventID: 4624
    condition: selection1 and selection2 and selection3
"""
        
        result_2 = transpiler.transpile(sigma_rule_2)
        print("Generated RML:")
        print(result_2)
        
        # Verify it's NOT using temporal monitor
        if "Monitor<start_ts" in result_2:
            print("FAIL: Three AND selections incorrectly using temporal monitor")
        else:
            print("PASS: Three AND selections correctly handled without temporal monitor")
        
        # Test Case 3: AND with OR
        print("\n--- Test Case 3: selection1 and (selection2 or selection3) ---")
        sigma_rule_3 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    selection3:
        EventID: 4624
    condition: selection1 and (selection2 or selection3)
"""
        
        result_3 = transpiler.transpile(sigma_rule_3)
        print("Generated RML:")
        print(result_3)
        
        # Verify it's NOT using temporal monitor
        if "Monitor<start_ts" in result_3:
            print("FAIL: AND with OR incorrectly using temporal monitor")
        else:
            print("PASS: AND with OR correctly handled without temporal monitor")
        
    except Exception as e:
        print(f"FAIL: Basic AND conditions test failed: {e}")
        import traceback
        traceback.print_exc()

def test_quantifier_patterns():
    """Test quantifier patterns like any of selection*, all of selection*"""
    print("\n=== Testing Quantifier Patterns ===")
    
    try:
        from app.core.transpiler_refactored import RefactoredTranspiler
        
        transpiler = RefactoredTranspiler()
        
        # Test Case 1: any of selection*
        print("\n--- Test Case 1: any of selection* ---")
        sigma_rule_1 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    selection3:
        EventID: 4624
    condition: any of selection*
"""
        
        result_1 = transpiler.transpile(sigma_rule_1)
        print("Generated RML:")
        print(result_1)
        
        # Verify it's NOT using temporal monitor
        if "Monitor<start_ts" in result_1:
            print("FAIL: any of selection* incorrectly using temporal monitor")
        else:
            print("PASS: any of selection* correctly handled without temporal monitor")
        
        # Test Case 2: all of selection*
        print("\n--- Test Case 2: all of selection* ---")
        sigma_rule_2 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    selection3:
        EventID: 4624
    condition: all of selection*
"""
        
        result_2 = transpiler.transpile(sigma_rule_2)
        print("Generated RML:")
        print(result_2)
        
        # Verify it's NOT using temporal monitor
        if "Monitor<start_ts" in result_2:
            print("FAIL: all of selection* incorrectly using temporal monitor")
        else:
            print("PASS: all of selection* correctly handled without temporal monitor")
        
        # Test Case 3: 2 of selection*
        print("\n--- Test Case 3: 2 of selection* ---")
        sigma_rule_3 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    selection3:
        EventID: 4624
    condition: 2 of selection*
"""
        
        result_3 = transpiler.transpile(sigma_rule_3)
        print("Generated RML:")
        print(result_3)
        
        # Verify it's NOT using temporal monitor
        if "Monitor<start_ts" in result_3:
            print("FAIL: 2 of selection* incorrectly using temporal monitor")
        else:
            print("PASS: 2 of selection* correctly handled without temporal monitor")
        
    except Exception as e:
        print(f"FAIL: Quantifier patterns test failed: {e}")
        import traceback
        traceback.print_exc()

def test_temporal_conditions():
    """Test that temporal conditions still work correctly"""
    print("\n=== Testing Temporal Conditions ===")
    
    try:
        from app.core.transpiler_refactored import RefactoredTranspiler
        
        transpiler = RefactoredTranspiler()
        
        # Test Case 1: Near operator (should use temporal monitor)
        print("\n--- Test Case 1: selection1 | near selection2 ---")
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
        print("Generated RML:")
        print(result_1)
        
        # Verify it IS using temporal monitor
        if "Monitor<start_ts" in result_1:
            print("PASS: Near operator correctly using temporal monitor")
        else:
            print("FAIL: Near operator not using temporal monitor")
        
        # Test Case 2: Near operator with timeframe (should use temporal monitor)
        print("\n--- Test Case 2: selection1 | near selection2 with timeframe ---")
        sigma_rule_2 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    timeframe: 5m
    condition: selection1 | near selection2
"""
        
        result_2 = transpiler.transpile(sigma_rule_2)
        print("Generated RML:")
        print(result_2)
        
        # Verify it IS using temporal monitor
        if "Monitor<start_ts" in result_2:
            print("PASS: Near operator with timeframe correctly using temporal monitor")
        else:
            print("FAIL: Near operator with timeframe not using temporal monitor")
        
    except Exception as e:
        print(f"FAIL: Temporal conditions test failed: {e}")
        import traceback
        traceback.print_exc()

def test_mixed_conditions():
    """Test mixed conditions to ensure they work correctly"""
    print("\n=== Testing Mixed Conditions ===")
    
    try:
        from app.core.transpiler_refactored import RefactoredTranspiler
        
        transpiler = RefactoredTranspiler()
        
        # Test Case 1: Basic condition with timeframe field but no temporal operators
        print("\n--- Test Case 1: Basic condition with timeframe field ---")
        sigma_rule_1 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    timeframe: 5m
    condition: selection1 and selection2
"""
        
        result_1 = transpiler.transpile(sigma_rule_1)
        print("Generated RML:")
        print(result_1)
        
        # Verify it's NOT using temporal monitor (timeframe field alone shouldn't trigger it)
        if "Monitor<start_ts" in result_1:
            print("FAIL: Basic condition with timeframe field incorrectly using temporal monitor")
        else:
            print("PASS: Basic condition with timeframe field correctly handled without temporal monitor")
        
        # Test Case 2: Complex condition with NOT
        print("\n--- Test Case 2: Complex condition with NOT ---")
        sigma_rule_2 = """
logsource:
    product: windows
    service: security
detection:
    selection1:
        EventID: 4698
    selection2:
        EventID: 4946
    selection3:
        EventID: 4624
    condition: selection1 and not selection2 and selection3
"""
        
        result_2 = transpiler.transpile(sigma_rule_2)
        print("Generated RML:")
        print(result_2)
        
        # Verify it's NOT using temporal monitor
        if "Monitor<start_ts" in result_2:
            print("FAIL: Complex condition with NOT incorrectly using temporal monitor")
        else:
            print("PASS: Complex condition with NOT correctly handled without temporal monitor")
        
    except Exception as e:
        print(f"FAIL: Mixed conditions test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all comprehensive basic pattern tests"""
    print("TEST: Comprehensive Basic Pattern Matching Test")
    print("=" * 80)
    
    try:
        test_basic_and_conditions()
        test_quantifier_patterns()
        test_temporal_conditions()
        test_mixed_conditions()
        
        print("\n" + "=" * 80)
        print("RESULT: Comprehensive Basic Pattern Test Completed!")
        print("PASS: All basic pattern scenarios tested")
        
    except Exception as e:
        print(f"\nFAIL: Comprehensive test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
