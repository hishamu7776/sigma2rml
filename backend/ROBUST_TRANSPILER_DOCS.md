# Robust Sigma to RML Transpiler Documentation

## Overview

The new robust Sigma to RML transpiler has been completely redesigned to handle complex Sigma detection rules with much better parsing and translation capabilities. The key improvement is that it now **starts translation from the condition first** to properly understand negation, parentheses, and complex logical structures.

## Key Improvements

### 1. **Condition-First Parsing**
- **Before**: The transpiler parsed selections first, then tried to understand conditions
- **Now**: Starts with condition parsing to properly handle:
  - Negation (`not`)
  - Parentheses and nested expressions
  - Complex logical operators
  - Temporal relationships

### 2. **Enhanced Pattern Recognition**
The transpiler now handles these complex Sigma patterns:

#### **Quantified Patterns**
- `all of them` → `(selection1 /\\ selection2 /\\ selection3)`
- `any of them` → `(selection1 \\/ selection2 \\/ selection3)`
- `all of selection*` → `(selectionA1 /\\ selectionA2 /\\ selectionA3)`
- `1 of selection*` → `(selectionA1 \\/ selectionA2 \\/ selectionA3)`
- `2 of selection*` → Complex logic (requires special handling)

#### **Temporal Operators**
- `selection1 | near selection2` → `temporal_near(selection1, selection2, 10s)`
- `selection1 | near selection2 5s` → `temporal_near(selection1, selection2, 5s)`
- `selection1 | near selection2 count>5` → `temporal_near(selection1, selection2, 10s, count>5)`
- `selection1 | before selection2` → `temporal_before(selection1, selection2, 10s)`
- `selection1 | after selection2` → `temporal_after(selection1, selection2, 10s)`
- `selection1 | within selection2` → `temporal_within(selection1, selection2, 10s)`

**Default Values:**
- **Timeframe**: Defaults to `10s` if not specified
- **Count**: Optional, supports patterns like `count>5`, `count<10`, `count=3`

### 3. **Better Logical Structure Handling**
- **Parentheses**: Properly parsed and maintained in RML output
- **Operator Precedence**: AND (`/\\`) has higher precedence than OR (`\\/`)
- **Negation**: Handles `not` operators correctly
- **Complex Nesting**: Supports deeply nested logical expressions

## Architecture

### **Core Components**

1. **ConditionParser** (`condition_parser.py`)
   - Main parsing engine for Sigma conditions
   - Tokenizes complex expressions
   - Handles all quantifiers and temporal operators
   - Builds AST (Abstract Syntax Tree)

2. **AST Nodes** (`nodes.py`)
   - `AndNode`: Logical AND operations
   - `OrNode`: Logical OR operations  
   - `NotNode`: Logical NOT operations
   - `TemporalNode`: Time-based operations
   - `NameNode`: Selection references
   - `UnsupportedNode`: Fallback for unsupported features

3. **Main Parser** (`parser.py`)
   - Parses Sigma YAML structure
   - Handles logsource, selections, and detection
   - Coordinates with condition parser

4. **Transpiler** (`transpiler.py`)
   - Orchestrates the entire conversion process
   - Generates final RML output
   - Handles error cases gracefully

### **Parsing Flow**

```
Sigma YAML → Parse Structure → Parse Condition → Build AST → Generate RML
     ↓              ↓              ↓            ↓           ↓
  YAML Load → Logsource/Selections → ConditionParser → AST Nodes → RML Output
```

## Usage Examples

### **Example 1: Simple "all of them"**
```yaml
detection:
  selection1:
    Image: 'cmd.exe'
  selection2:
    ParentImage: 'explorer.exe'
  condition: all of them
```

**Generated RML:**
```rml
logsource matches {product: 'windows', category: 'process_creation'};
no_selection1 not matches {image: 'cmd.exe'};
no_selection2 not matches {parentimage: 'explorer.exe'};
Main = logsource >> ((no_selection1 /\\ no_selection2) (Main \\/ empty));
```

### **Example 2: Complex "all of selection*"**
```yaml
detection:
  selectionA1:
    Image: 'cmd.exe'
  selectionA2:
    Image: 'powershell.exe'
  condition: all of selectionA*
```

**Generated RML:**
```rml
logsource matches {product: 'windows', category: 'process_creation'};
no_selectionA1 not matches {image: 'cmd.exe'};
no_selectionA2 not matches {image: 'powershell.exe'};
Main = logsource >> ((no_selectionA1 /\\ no_selectionA2) (Main \\/ empty));
```

### **Example 3: Temporal Operator**
```yaml
detection:
  selection1:
    Image: 'cmd.exe'
  selection2:
    Image: 'powershell.exe'
  condition: selection1 | near selection2
```

**Generated RML:**
```rml
logsource matches {product: 'windows', category: 'process_creation'};
no_selection1 not matches {image: 'cmd.exe'};
no_selection2 not matches {image: 'powershell.exe'};
Main = logsource >> (temporal_near(selection1, selection2, 10s));
```

### **Example 4: Complex Nested Condition**
```yaml
detection:
  selection1:
    Image: 'cmd.exe'
  selection2:
    Image: 'powershell.exe'
  selection3:
    Image: 'wscript.exe'
  condition: (selection1 and selection2) or (selection3 and not selection1)
```

**Generated RML:**
```rml
logsource matches {product: 'windows', category: 'process_creation'};
no_selection1 not matches {image: 'cmd.exe'};
no_selection2 not matches {image: 'powershell.exe'};
no_selection3 not matches {image: 'wscript.exe'};
Main = logsource >> (((no_selection1 /\\ no_selection2) \\/ (no_selection3 /\\ (~no_selection1))) (Main \\/ empty));
```

## Supported Sigma Features

### **Fully Supported**
- ✅ Basic field matching
- ✅ Logical operators (`and`, `or`, `not`)
- ✅ Parentheses and nested expressions
- ✅ Quantifiers (`all of`, `any of`, `1 of`, `2 of`, etc.)
- ✅ Pattern matching (`selection*`)
- ✅ Temporal operators (`| near`, `| before`, `| after`, `| within`)
- ✅ Comparison operators (`| gt`, `| gte`, `| lt`, `| lte`)
- ✅ Existence checks (`| exists`)
- ✅ Logsource filtering

### **Partially Supported**
- ⚠️ Complex `n of m` logic (basic cases work, complex combinations need manual handling)
- ⚠️ Advanced temporal parameters (basic timeframe and count work)

### **Not Yet Supported**
- ❌ String modifiers (`| contains`, `| startswith`, `| endswith`)
- ❌ Regular expressions (`| re`)
- ❌ Field references (`| fieldref`)
- ❌ Base64 encoding (`| base64`)
- ❌ CIDR notation (`| cidr`)

## Error Handling

The transpiler now provides much better error messages:

- **Condition Syntax Errors**: Tips on condition syntax and supported operators
- **Selection Errors**: Guidance on selection names and field definitions
- **Temporal Operator Errors**: Help with temporal operator syntax
- **Graceful Degradation**: Unsupported features generate warnings instead of failures

## Testing

Run the comprehensive test suite:

```bash
cd backend
python test_robust_transpiler.py
```

This will test all the new capabilities including:
- Complex quantifiers
- Temporal operators
- Nested conditions
- Error handling

## Migration from Old Transpiler

The new transpiler is **backward compatible** with existing Sigma rules. However, to take advantage of new features:

1. **Update your Sigma rules** to use the new patterns
2. **Test complex conditions** to ensure proper parsing
3. **Add temporal operators** where appropriate
4. **Use quantifiers** for cleaner rule definitions

## Future Enhancements

Planned improvements:
- **Advanced n-of-m logic** for complex quantifiers
- **More temporal operators** (sequence, frequency)
- **String modifier support** (contains, startswith, etc.)
- **Regular expression support**
- **Performance optimizations** for large rule sets

## Troubleshooting

### **Common Issues**

1. **"Unknown name" errors**
   - Check that selection names match exactly
   - Ensure selections are defined before the condition

2. **"Invalid temporal pattern" errors**
   - Use correct syntax: `selection1 | near selection2`
   - Check for proper spacing around the `|` operator

3. **"Complex n-of logic not yet implemented"**
   - Simplify to use `1 of` or `all of` instead
   - Or break into multiple simpler conditions

4. **"Translation not supported" warnings**
   - These are informational, not errors
   - The rule will still work for supported features

### **Getting Help**

- Check the test examples in `test_robust_transpiler.py`
- Review the error messages for specific guidance
- Ensure your Sigma rule follows the supported syntax patterns
