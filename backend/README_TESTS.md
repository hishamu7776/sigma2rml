# Sigma to RML Transpiler - Test Structure

## 📁 Directory Structure

```
backend/
├── tests/                          # Organized test files
│   ├── __init__.py
│   ├── test_basic_patterns.py     # Basic Sigma patterns
│   ├── test_quantifiers.py        # Quantifier patterns
│   ├── test_temporal_operators.py # Temporal operators
│   ├── test_complex_conditions.py # Complex conditions
│   └── test_all.py                # Comprehensive test runner
├── debug/                          # Debug utilities
│   ├── __init__.py
│   ├── debug_quantifiers.py       # Debug quantifier parsing
│   └── debug_temporal.py          # Debug temporal operators
└── README_TESTS.md                # This file
```

## 🧪 Test Categories

### 1. Basic Patterns (`test_basic_patterns.py`)
- Simple selections
- Multiple EventIDs
- Basic logical operators (and, or, not)
- OR conditions

### 2. Quantifiers (`test_quantifiers.py`)
- `all of them`
- `all of selection*`
- `1 of selection*`
- `N of selection*` (where N > 1)

### 3. Temporal Operators (`test_temporal_operators.py`)
- `selection1 | near selection2` (with and without timeframe)
- `selection1 and selection2` with timeframe
- `selection1 and selection2 and selection3` with timeframe
- `all of selection*` with timeframe
- `selection | count() > N`

### 4. Complex Conditions (`test_complex_conditions.py`)
- Complex nested conditions with NOT
- Multiple filters with complex logic
- Comparison operators (lte, gte, etc.)
- Edge cases and error handling

## 🚀 Running Tests

### Run All Tests
```bash
cd backend
python tests/test_all.py
```

### Run Specific Test Categories
```bash
cd backend
python tests/test_basic_patterns.py
python tests/test_quantifiers.py
python tests/test_temporal_operators.py
python tests/test_complex_conditions.py
```

### Debug Specific Issues
```bash
cd backend
python debug/debug_quantifiers.py
python debug/debug_temporal.py
```

## 🔍 Debug Utilities

### `debug_quantifiers.py`
- Tests all quantifier patterns
- Shows tokenization and parsing results
- Helps debug quantifier expansion issues

### `debug_temporal.py`
- Tests temporal operator parsing
- Shows how `| near`, `| count()` are handled
- Helps debug timeframe and count operator issues

## 📋 Test Coverage

The test suite covers all the scenarios mentioned in your SigmaToRML.docx document:

✅ **Basic Patterns**: Simple selections, multiple EventIDs  
✅ **Quantifiers**: `all of them`, `all of selection*`, `1 of selection*`  
✅ **Temporal Operators**: `| near`, `| count()`, timeframe handling  
✅ **Complex Logic**: AND/OR combinations, NOT operations, parentheses  
✅ **Edge Cases**: Empty conditions, invalid YAML, comparison operators  

## 🎯 Next Steps

1. **Implement Missing Features**: Temporal operators, count operators
2. **Update Transpiler**: Handle timeframe and count scenarios
3. **Test Integration**: Ensure all patterns work together
4. **Frontend Updates**: Reflect backend improvements in UI

## 💡 Development Tips

- Use `debug_*.py` scripts to isolate parsing issues
- Run individual test files during development
- Use `test_all.py` for comprehensive validation
- Check tokenization output when debugging parsing issues
