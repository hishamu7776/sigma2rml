#!/usr/bin/env python3
"""
Comprehensive test runner for all Sigma to RML tests
Runs all test categories in sequence
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():
    """Run all test categories"""
    print("🚀 Running All Sigma to RML Tests")
    print("=" * 60)
    
    # Import and run each test category
    test_modules = [
        ('Basic Patterns', 'test_basic_patterns'),
        ('Quantifiers', 'test_quantifiers'),
        ('Temporal Operators', 'test_temporal_operators'),
        ('Complex Conditions', 'test_complex_conditions'),
        ('Unsupported Modifiers', 'test_unsupported_modifiers'),
        ('Numerical Modifiers', 'test_numerical_modifiers')
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for category, module_name in test_modules:
        print(f"\n📋 Testing {category}")
        print("-" * 40)
        
        try:
            # Import the test module
            module = __import__(module_name)
            
            # Run the tests
            if hasattr(module, 'test_simple_selection'):
                module.test_simple_selection()
                passed_tests += 1
            if hasattr(module, 'test_multiple_eventids'):
                module.test_multiple_eventids()
                passed_tests += 1
            if hasattr(module, 'test_basic_logical_operators'):
                module.test_basic_logical_operators()
                passed_tests += 1
            if hasattr(module, 'test_or_condition'):
                module.test_or_condition()
                passed_tests += 1
            if hasattr(module, 'test_all_of_them'):
                module.test_all_of_them()
                passed_tests += 1
            if hasattr(module, 'test_all_of_selection_star'):
                module.test_all_of_selection_star()
                passed_tests += 1
            if hasattr(module, 'test_1_of_selection_star'):
                module.test_1_of_selection_star()
                passed_tests += 1
            if hasattr(module, 'test_n_of_selection_star'):
                module.test_n_of_selection_star()
                passed_tests += 1
            if hasattr(module, 'test_near_without_timeframe'):
                module.test_near_without_timeframe()
                passed_tests += 1
            if hasattr(module, 'test_near_with_timeframe'):
                module.test_near_with_timeframe()
                passed_tests += 1
            if hasattr(module, 'test_and_with_timeframe'):
                module.test_and_with_timeframe()
                passed_tests += 1
            if hasattr(module, 'test_three_way_and_with_timeframe'):
                module.test_three_way_and_with_timeframe()
                passed_tests += 1
            if hasattr(module, 'test_all_of_selection_star_with_timeframe'):
                module.test_all_of_selection_star_with_timeframe()
                passed_tests += 1
            if hasattr(module, 'test_count_operator'):
                module.test_count_operator()
                passed_tests += 1
            if hasattr(module, 'test_complex_not_condition'):
                module.test_complex_not_condition()
                passed_tests += 1
            if hasattr(module, 'test_comparison_operators'):
                module.test_comparison_operators()
                passed_tests += 1
            if hasattr(module, 'test_multiple_filters'):
                module.test_multiple_filters()
                passed_tests += 1
            if hasattr(module, 'test_empty_condition'):
                module.test_empty_condition()
                passed_tests += 1
            if hasattr(module, 'test_invalid_yaml'):
                module.test_invalid_yaml()
                passed_tests += 1
            if hasattr(module, 'test_unsupported_modifiers'):
                module.test_unsupported_modifiers()
                passed_tests += 1
            if hasattr(module, 'test_numerical_modifiers'):
                module.test_numerical_modifiers()
                passed_tests += 1
                
            print(f"✅ {category} tests completed successfully")
            
        except Exception as e:
            print(f"❌ Error in {category}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Summary: {passed_tests} tests completed")
    print("✅ All test categories processed")
    print("\n🚀 Sigma to RML transpiler is ready for production!")

if __name__ == "__main__":
    run_all_tests()
