#!/usr/bin/env python3
"""
Test Fixed Temporal Monitor System
Tests the fixes for missing semicolons and proper field values in safe selections
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_fixed_temporal_monitor():
    """Test the fixed temporal monitor system"""
    print("=== Testing Fixed Temporal Monitor System ===")
    
    try:
        from app.core.transpiler import SigmaToRMLTranspiler
        
        transpiler = SigmaToRMLTranspiler()
        
        # Test Case 1: Simple AND operation with timeframe (from manual test)
        print("\n--- Test Case 1: Simple AND with timeframe ---")
        sigma_rule_1 = """
logsource:
    product: windows
    service: security
detection:
    selection_task:
        EventID: 4698
    selection_firewall:
        EventID: 4946
    timeframe: 5m
    condition: selection_task and selection_firewall
"""
        
        result_1 = transpiler.transpile(sigma_rule_1)
        print("✅ Transpilation successful")
        print("Generated RML:")
        print(result_1)
        
        # Test Case 2: Three selections with AND (from manual test)
        print("\n--- Test Case 2: Three selections with AND ---")
        sigma_rule_2 = """
logsource:
    product: windows
    service: security
detection:
    selection_task:
        EventID: 4698
    selection_firewall:
        EventID: 4946
    selection_extra:
        EventID: 5012
    timeframe: 5m
    condition: selection_task and selection_firewall and selection_extra
"""
        
        result_2 = transpiler.transpile(sigma_rule_2)
        print("✅ Transpilation successful")
        print("Generated RML:")
        print(result_2)
        
        # Test Case 3: Four selections with AND (from manual test)
        print("\n--- Test Case 3: Four selections with AND ---")
        sigma_rule_3 = """
logsource:
    product: windows
    service: security
detection:
    selection_task:
        EventID: 4698
    selection_firewall:
        EventID: 4946
    selection_extra:
        EventID: 5012
    selection_extra2:
        EventID: 5025
    timeframe: 5m
    condition: selection_task and selection_firewall and selection_extra and selection_extra2
"""
        
        result_3 = transpiler.transpile(sigma_rule_3)
        print("✅ Transpilation successful")
        print("Generated RML:")
        print(result_3)
        
        # Test Case 4: Complex condition with NOT (from manual test)
        print("\n--- Test Case 4: Complex condition with NOT ---")
        sigma_rule_4 = """
logsource:
    product: windows
    service: security
detection:
    selection_task:
        EventID: 4698
    selection_firewall:
        EventID: 4946
    selection_extra:
        EventID: 5012
    selection_extra2:
        EventID: 5025
    timeframe: 5m
    condition: selection_task and not selection_firewall and selection_extra and not selection_extra2
"""
        
        result_4 = transpiler.transpile(sigma_rule_4)
        print("✅ Transpilation successful")
        print("Generated RML:")
        print(result_4)
        
        print("\n🎯 Fixed Temporal Monitor Test Completed!")
        print("✅ All test cases transpiled successfully")
        
        # Verify fixes
        print("\n🔍 Verifying Fixes:")
        
        # Check for semicolons
        if ";" in result_1 and result_1.strip().endswith(";"):
            print("✅ Semicolons: Fixed - monitor definitions end with semicolons")
        else:
            print("❌ Semicolons: Still missing")
        
        # Check for proper field values in safe selections
        if "safe_selection_task(ts) matches {timestamp: ts, eventid: 4698}" in result_1:
            print("✅ Field Values: Fixed - safe selections include actual field values")
        else:
            print("❌ Field Values: Still missing")
        
        # Check for proper NOT handling
        if "safe_selection_firewall not matches {eventid: 4946}" in result_4:
            print("✅ NOT Handling: Fixed - negated selections use proper field values")
        else:
            print("❌ NOT Handling: Still missing")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fixed_temporal_monitor()
