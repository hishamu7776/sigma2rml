#!/usr/bin/env python3
"""
Test Enhanced Temporal Monitor System
Tests the new temporal monitor translation for complex Sigma conditions
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_enhanced_temporal_monitor():
    """Test the enhanced temporal monitor system"""
    print("=== Testing Enhanced Temporal Monitor System ===")
    
    try:
        from app.core.transpiler import SigmaToRMLTranspiler
        
        transpiler = SigmaToRMLTranspiler()
        
        # Test Case 1: Simple AND operation with timeframe
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
        
        # Test Case 2: Three selections with AND
        print("\n--- Test Case 2: Three selections with AND ---")
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
    timeframe: 10m
    condition: selection1 and selection2 and selection3
"""
        
        result_2 = transpiler.transpile(sigma_rule_2)
        print("✅ Transpilation successful")
        print("Generated RML:")
        print(result_2)
        
        # Test Case 3: Complex condition with NOT
        print("\n--- Test Case 3: Complex condition with NOT ---")
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
    timeframe: 2m
    condition: selection1 and (selection2 or not selection3)
"""
        
        result_3 = transpiler.transpile(sigma_rule_3)
        print("✅ Transpilation successful")
        print("Generated RML:")
        print(result_3)
        
        # Test Case 4: Near operator (should be equivalent to AND with timeframe)
        print("\n--- Test Case 4: Near operator ---")
        sigma_rule_4 = """
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
        
        result_4 = transpiler.transpile(sigma_rule_4)
        print("✅ Transpilation successful")
        print("Generated RML:")
        print(result_4)
        
        print("\n🎯 Enhanced Temporal Monitor Test Completed!")
        print("✅ All test cases transpiled successfully")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

def test_timeframe_parsing():
    """Test timeframe parsing functionality"""
    print("\n=== Testing Timeframe Parsing ===")
    
    try:
        from app.core.ast.temporal_monitor import TemporalMonitorGenerator
        
        generator = TemporalMonitorGenerator()
        
        test_timeframes = [
            "5s", "10m", "2h", "1d",
            "30s", "15m", "3h", "7d"
        ]
        
        for timeframe in test_timeframes:
            ms = generator.parse_timeframe(timeframe)
            print(f"✅ {timeframe} -> {ms}ms")
        
        print("🎯 Timeframe parsing test completed!")
        
    except Exception as e:
        print(f"❌ Timeframe parsing test failed: {e}")

def test_selection_extraction():
    """Test selection extraction from complex conditions"""
    print("\n=== Testing Selection Extraction ===")
    
    try:
        from app.core.ast.temporal_monitor import TemporalMonitorGenerator
        from app.core.ast.nodes import NameNode, AndNode, OrNode, NotNode
        
        generator = TemporalMonitorGenerator()
        
        # Create a complex condition: selection1 and (selection2 or not selection3)
        selection1 = NameNode("selection1")
        selection2 = NameNode("selection2")
        selection3 = NameNode("selection3")
        not_selection3 = NotNode(selection3)
        or_node = OrNode(selection2, not_selection3)
        and_node = AndNode(selection1, or_node)
        
        selections = generator.extract_selections_from_condition(and_node)
        
        print("✅ Extracted selections:")
        for name, is_negated in selections:
            status = "NOT" if is_negated else "POSITIVE"
            print(f"   {name}: {status}")
        
        print("🎯 Selection extraction test completed!")
        
    except Exception as e:
        print(f"❌ Selection extraction test failed: {e}")

if __name__ == "__main__":
    test_enhanced_temporal_monitor()
    test_timeframe_parsing()
    test_selection_extraction()
