#!/usr/bin/env python3
"""
Test transpiler core functionality
- Simple selections
- Logsource and selection combinations
- Various modifiers and conditions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.transpiler_refactored import RefactoredTranspiler

def test_simple_selection():
    """Test simple selection pattern"""
    print("=== Simple Selection Test ===")
    
    sigma = """
detection:
  selection:
    Image: '\\example.exe'
    Description: 'Test executable'
  condition: selection
"""
    transpiler = RefactoredTranspiler()
    rml = transpiler.transpile(sigma)
    print(rml)
    print()

def test_logsource_and_selection():
    """Test logsource and selection combination"""
    print("=== Logsource and Selection Test ===")
    
    sigma = """
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    Image: '\\cmd.exe'
  condition: selection
"""
    transpiler = RefactoredTranspiler()
    rml = transpiler.transpile(sigma)
    print(rml)
    print()

def test_exists_modifier():
    """Test exists modifier"""
    print("=== Exists Modifier Test ===")
    
    sigma = """
detection:
  selection:
    EventID: 4738
    PasswordLastSet|exists: true
  condition: selection
"""
    transpiler = RefactoredTranspiler()
    rml = transpiler.transpile(sigma)
    print(rml)
    print()

def test_gt_modifier():
    """Test greater than modifier"""
    print("=== GT Modifier Test ===")
    
    sigma = """
detection:
  selection:
    EventID|gt: 4000
  condition: selection
"""
    transpiler = RefactoredTranspiler()
    rml = transpiler.transpile(sigma)
    print(rml)
    print()

def test_selection_and_not_filter():
    """Test selection with NOT filter"""
    print("=== Selection and NOT Filter Test ===")
    
    sigma = """
detection:
  selection:
    EventID: 4738
  filter:
    PasswordLastSet: null
  condition: selection and not filter
"""
    transpiler = RefactoredTranspiler()
    rml = transpiler.transpile(sigma)
    print(rml)
    print()

def test_selection_list_values():
    """Test selection with list values"""
    print("=== Selection List Values Test ===")
    
    sigma = """
detection:
  selection:
    EventID:
      - 517
      - 1102
  condition: selection
"""
    transpiler = RefactoredTranspiler()
    rml = transpiler.transpile(sigma)
    print(rml)
    print()

def test_unsupported_keywords():
    """Test unsupported keywords handling"""
    print("=== Unsupported Keywords Test ===")
    
    sigma = """
detection:
  keywords:
    - 'mimikatz'
    - 'sekurlsa'
  condition: keywords
"""
    transpiler = RefactoredTranspiler()
    rml = transpiler.transpile(sigma)
    print(rml)
    print()

if __name__ == "__main__":
    print("Testing Transpiler Core Functionality")
    print("=" * 50)
    
    test_simple_selection()
    test_logsource_and_selection()
    test_exists_modifier()
    test_gt_modifier()
    test_selection_and_not_filter()
    test_selection_list_values()
    test_unsupported_keywords()
    
    print("Transpiler core tests completed!")
