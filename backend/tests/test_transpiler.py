# tests/test_transpiler.py

import pytest
from app.core.transpiler import SigmaToRMLTranspiler

transpiler = SigmaToRMLTranspiler()

# --- Supported cases ---

def test_simple_selection():
    sigma = """
detection:
  selection:
    Image: '\\example.exe'
    Description: 'Test executable'
  condition: selection
"""
    rml = transpiler.transpile(sigma)
    assert "no_selection not matches" in rml
    assert "Main = (no_selection (Main \\/ empty));" in rml

def test_logsource_and_selection():
    sigma = """
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    Image: '\\cmd.exe'
  condition: selection
"""
    rml = transpiler.transpile(sigma)
    assert "logsourceFilter() matches" in rml
    assert "no_selection not matches" in rml
    assert "logsourceFilter >> (no_selection (Main \\/ empty))" in rml

def test_exists_modifier():
    sigma = """
detection:
  selection:
    EventID: 4738
    PasswordLastSet|exists: true
  condition: selection
"""
    rml = transpiler.transpile(sigma)
    assert "exists matches" in rml
    assert "no_selection not matches" in rml
    assert "exists >> (no_selection (Main \\/ empty))" in rml

def test_gt_modifier():
    sigma = """
detection:
  selection:
    EventID|gt: 4000
  condition: selection
"""
    rml = transpiler.transpile(sigma)
    assert "> 4000" in rml or "gt" in rml

def test_selection_and_not_filter():
    sigma = """
detection:
  selection:
    EventID: 4738
  filter:
    PasswordLastSet: null
  condition: selection and not filter
"""
    rml = transpiler.transpile(sigma)
    assert "no_selection not matches" in rml
    assert "filter matches" in rml
    assert "/\\" in rml  # and operator

def test_selection_list_values():
    sigma = """
detection:
  selection:
    EventID:
      - 517
      - 1102
  condition: selection
"""
    rml = transpiler.transpile(sigma)
    assert "no_selection_1 not matches" in rml
    assert "no_selection_2 not matches" in rml
    assert "\\/" in rml  # or operator

# --- Unsupported cases ---

def test_unsupported_keywords():
    sigma = """
detection:
  keywords:
    - 'mimikatz'
    - 'sekurlsa'
  condition: keywords
"""
    rml = transpiler.transpile(sigma)
    assert "// Translation not supported" in rml

def test_unsupported_contains_modifier():
    sigma = """
detection:
  selection:
    field|contains: 'evil.exe'
  condition: selection
"""
    rml = transpiler.transpile(sigma)
    assert "// Translation not supported" in rml

def test_any_of_selection_star():
    sigma = """
detection:
  selection1:
    field1: 'value1'
  selection2:
    field2: 'value2'
  condition: 1 of selection*
"""
    rml = transpiler.transpile(sigma)
    assert "\\/" in rml  # or across selections
