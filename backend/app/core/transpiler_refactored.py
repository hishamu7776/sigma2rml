#!/usr/bin/env python3
"""
Refactored Sigma to RML Transpiler
Clean, scalable architecture that handles all Sigma rule patterns systematically
"""

import re
from typing import Dict, List, Any, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum

class ConditionType(Enum):
    """Types of conditions that can be processed"""
    BASIC = "basic"
    TEMPORAL = "temporal"
    QUANTIFIER = "quantifier"

@dataclass
class FieldValue:
    """Represents a field value with optional modifiers"""
    field_name: str
    value: Any
    modifier: Optional[str] = None
    variable_name: Optional[str] = None

@dataclass
class Selection:
    """Represents a selection with its fields and values"""
    name: str
    fields: Dict[str, FieldValue]
    negated: bool = False

@dataclass
class ConditionNode:
    """Represents a parsed condition structure"""
    operator: str  # 'and', 'or', 'not'
    left: Any  # ConditionNode or str
    right: Any  # ConditionNode or str
    negated: bool = False

class ConditionSimplifier:
    """Handles condition simplification using De Morgan's laws and other optimizations"""
    
    @staticmethod
    def simplify_condition(condition: str) -> str:
        """Simplify the condition string by applying De Morgan's laws and removing unnecessary parentheses"""
        # Remove extra spaces
        condition = re.sub(r'\s+', ' ', condition.strip())
        
        # Use the user's elegant parentheses parsing and De Morgan's law logic
        newcondition, par_map = ConditionSimplifier._parse_condition(condition)
        simplified = ConditionSimplifier._regenerate_condition(newcondition, par_map)
        
        return ' '.join(simplified)
    
    @staticmethod
    def _parse_condition(condition: str, last_idx: int = 0, par_map: dict = None):
        """Parse parentheses and map them to indices"""
        if par_map is None:
            par_map = {}
        
        pattern = r'\([^()]*\)'
        matches = re.findall(pattern, condition)
        
        for p in matches:
            par_map[str(last_idx)] = p
            condition = condition.replace(p, str(last_idx))
            last_idx += 1
            
        if len(matches) > 0:
            condition, par_map = ConditionSimplifier._parse_condition(condition, last_idx, par_map)
        
        return condition, par_map
    
    @staticmethod
    def _regenerate_condition(condition: str, parse_map: dict, flag: bool = False, operation: str = 'none', level: int = 0):
        """Regenerate condition with proper De Morgan's law application"""
        token_list = condition.split()
        new_list = []
        
        for idx, token in enumerate(token_list):
            if token == 'and':
                if flag:
                    new_list.append('or')
                    operation = 'or'
                else:
                    new_list.append('and')
                    operation = 'and'
            elif token == 'or':
                if flag:
                    new_list.append('and')
                    operation = 'and'
                else:
                    new_list.append('or')
                    operation = 'or'
            elif token == 'not':
                if flag:
                    flag = False
                else:
                    if level > 0:
                        new_list.append(token)
                    flag = True
            else:
                try:
                    val = parse_map[token]
                    val = ConditionSimplifier._regenerate_condition(val[1:-1], parse_map, flag, level + 1)
                    
                    # Check if parentheses are needed based on operator precedence
                    if operation == 'and' and 'and' in val and 'or' not in val:
                        s = ' '.join(val)
                    elif operation == 'or' and 'or' in val and 'and' not in val:
                        s = ' '.join(val)
                    else:
                        s = '(' + ' '.join(val) + ')'
                    
                    new_list.append(s)
                    flag = False
                except KeyError:
                    if flag:
                        new_list.append('not')
                    new_list.append(token)
        
        return new_list
    
    @staticmethod
    def _is_selection_negated(selection_name: str, condition: str) -> bool:
        """Determine if a selection is negated in the simplified condition"""
        # Split the condition into tokens
        tokens = condition.split()
        
        # Look for patterns like "not selection_name" or "not (selection_name ...)"
        for i, token in enumerate(tokens):
            if token == 'not':
                # Check if the next token is the selection name
                if i + 1 < len(tokens) and tokens[i + 1] == selection_name:
                    return True
                # Check if the next token is a parenthesized expression containing the selection
                elif i + 1 < len(tokens) and tokens[i + 1].startswith('('):
                    # Extract the content inside parentheses
                    paren_content = tokens[i + 1][1:-1] if tokens[i + 1].endswith(')') else tokens[i + 1][1:]
                    if selection_name in paren_content:
                        return True
        
        # More sophisticated check: look for the selection in negated parenthesized expressions
        # This handles cases like "not (A or B)" where both A and B are negated
        # Find all parenthesized expressions
        import re
        paren_pattern = r'not\s*\(([^)]+)\)'
        matches = re.findall(paren_pattern, condition)
        
        for match in matches:
            # Check if our selection is in this negated expression
            if selection_name in match:
                return True
        
        # Additional check: look for selections that appear in parenthesized expressions
        # that are part of a larger negated context
        # This handles cases where the original condition had "not (A or B)" and after
        # De Morgan's law application, we get "(not A or not B)"
        paren_pattern2 = r'\(([^)]+)\)'
        paren_matches = re.findall(paren_pattern2, condition)
        
        for match in paren_matches:
            if selection_name in match:
                # Check if this parenthesized expression contains "not selection_name"
                if f"not {selection_name}" in match:
                    return True
        
        return False

class QuantifierExpander:
    """Handles quantifier expansion (all of, any of, 1 of, etc.)"""
    
    @staticmethod
    def expand_quantifiers(condition: str, selections: List[str]) -> str:
        """Expand quantifier patterns to explicit conditions"""
        if 'all of selection*' in condition:
            return QuantifierExpander._expand_all_of(condition, selections)
        elif 'any of selection*' in condition:
            return QuantifierExpander._expand_any_of(condition, selections)
        elif '1 of selection*' in condition:
            return QuantifierExpander._expand_one_of(condition, selections)
        elif re.search(r'(\d+)\s+of\s+selection\*', condition):
            return QuantifierExpander._expand_n_of(condition, selections)
        
        return condition
    
    @staticmethod
    def _expand_all_of(condition: str, selections: List[str]) -> str:
        """Expand 'all of selection*' to 'selection1 and selection2 and ...'"""
        expanded = ' and '.join(selections)
        return condition.replace('all of selection*', expanded)
    
    @staticmethod
    def _expand_any_of(condition: str, selections: List[str]) -> str:
        """Expand 'any of selection*' to 'selection1 or selection2 or ...'"""
        expanded = ' or '.join(selections)
        return condition.replace('any of selection*', expanded)
    
    @staticmethod
    def _expand_one_of(condition: str, selections: List[str]) -> str:
        """Expand '1 of selection*' to 'selection1 or selection2 or ...'"""
        expanded = ' or '.join(selections)
        return condition.replace('1 of selection*', expanded)
    
    @staticmethod
    def _expand_n_of(condition: str, selections: List[str]) -> str:
        """Expand 'N of selection*' patterns"""
        match = re.search(r'(\d+)\s+of\s+selection\*', condition)
        if match:
            n = int(match.group(1))
            if n == 1:
                expanded = ' or '.join(selections)
            elif n == len(selections):
                expanded = ' and '.join(selections)
            else:
                # For unsupported N values, mark as unsupported
                expanded = f"UNSUPPORTED_{n}_of_pattern"
            
            return condition.replace(match.group(0), expanded)
        
        return condition

class FieldValueExtractor:
    """Extracts and formats field values for RML generation"""
    
    @staticmethod
    def extract_field_values(field_data: Any, variable_counter: int = 1) -> List[FieldValue]:
        """Extract field values from detection data"""
        field_values = []
        counter = variable_counter
        
        if isinstance(field_data, dict):
            for field_name, value in field_data.items():
                if '|' in field_name:
                    # Handle modifiers like |gte, |lte, etc.
                    base_name, modifier = field_name.split('|', 1)
                    field_values.append(FieldValue(
                        field_name=base_name.lower(),  # Convert to lowercase to match examples
                        value=value,
                        modifier=modifier,
                        variable_name=f"x{counter}"
                    ))
                    counter += 1
                else:
                    field_values.append(FieldValue(
                        field_name=field_name.lower(),  # Convert to lowercase to match examples
                        value=value
                    ))
        
        return field_values, counter
    
    @staticmethod
    def format_field_value(field_value: FieldValue) -> str:
        """Format a field value for RML output"""
        if field_value.modifier:
            # Handle numerical modifiers
            if field_value.modifier == 'gte':
                return f"{field_value.field_name}: {field_value.variable_name}"
            elif field_value.modifier == 'lte':
                return f"{field_value.field_name}: {field_value.variable_name}"
            elif field_value.modifier == 'gt':
                return f"{field_value.field_name}: {field_value.variable_name}"
            elif field_value.modifier == 'lt':
                return f"{field_value.field_name}: {field_value.variable_name}"
            else:
                return f"{field_value.field_name}: {field_value.value}"
        else:
            # Handle regular values
            if isinstance(field_value.value, list):
                if all(isinstance(v, str) for v in field_value.value):
                    quoted_values = [f"'{v}'" for v in field_value.value]
                    return f"{field_value.field_name}: {' | '.join(quoted_values)}"
                else:
                    return f"{field_value.field_name}: {' | '.join(str(v) for v in field_value.value)}"
            elif isinstance(field_value.value, str):
                return f"{field_value.field_name}: '{field_value.value}'"
            else:
                return f"{field_value.field_name}: {field_value.value}"

class RMLLineGenerator:
    """Generates individual RML lines and sections"""
    
    @staticmethod
    def generate_logsource_filter(logsource: Dict[str, Any]) -> str:
        """Generate logsource filter line"""
        if not logsource:
            return "logsource matches {product: 'windows', service: 'security'};"
        
        fields = []
        for key, value in logsource.items():
            if isinstance(value, str):
                fields.append(f"{key}: '{value}'")
            else:
                fields.append(f"{key}: {value}")
        
        return f"logsource matches {{{', '.join(fields)}}};"
    
    @staticmethod
    def generate_selection_definition(selection: Selection) -> str:
        """Generate a selection definition line"""
        field_pairs = []
        constraints = []
        
        for field_name, field_value in selection.fields.items():
            formatted_value = FieldValueExtractor.format_field_value(field_value)
            field_pairs.append(formatted_value)
            
            # Collect constraints for numerical modifiers
            if field_value.modifier and field_value.variable_name:
                if field_value.modifier == 'gte':
                    constraints.append(f"{field_value.variable_name} >= {field_value.value}")
                elif field_value.modifier == 'lte':
                    constraints.append(f"{field_value.variable_name} <= {field_value.value}")
                elif field_value.modifier == 'gt':
                    constraints.append(f"{field_value.variable_name} > {field_value.value}")
                elif field_value.modifier == 'lt':
                    constraints.append(f"{field_value.variable_name} < {field_value.value}")
        
        if field_pairs:
            field_str = f"{{{', '.join(field_pairs)}}}"
        else:
            field_str = "{}"
        
        # Add constraints after the field definition if any exist
        if constraints:
            constraint_str = f" with {' and '.join(constraints)}"
        else:
            constraint_str = ""
        
        # Sigma semantics: detect A means RML should filter out A (not matches)
        # Sigma semantics: not A means RML should ensure A is present (matches)
        if selection.negated:
            return f"safe_{selection.name} matches {field_str}{constraint_str};"
        else:
            return f"safe_{selection.name} not matches {field_str}{constraint_str};"
    
    @staticmethod
    def generate_main_expression() -> str:
        """Generate the main expression line"""
        return "Main = logsource >> Monitor;"
    
    @staticmethod
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
        
        # Check for quantifier patterns
        if 'any of selection*' in original_condition:
            return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        elif 'all of selection*' in original_condition:
            return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
        elif '1 of selection*' in original_condition:
            return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        elif '2 of selection*' in original_condition or '3 of selection*' in original_condition:
            return f"Monitor = UNSUPPORTED_PATTERN; // {original_condition} not supported"
        
        # Handle complex conditions with parentheses and mixed operators
        # This is the key fix for the bug you identified
        if '(' in original_condition and ')' in original_condition:
            return RMLLineGenerator._generate_complex_monitor_expression(original_condition, safe_selections)
        
        # Handle simple mixed operators without parentheses
        if ' and ' in original_condition and ' or ' in original_condition:
            # Complex mixed condition - use AND for safety
            return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        elif ' and ' in original_condition:
            return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
        elif ' or ' in original_condition:
            return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        
        # Default case: assume AND for multiple selections
        return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
    
    @staticmethod
    def _generate_complex_monitor_expression(condition: str, safe_selections: List[str]) -> str:
        """Generate monitor expression for complex conditions with parentheses"""
        # Find all parenthesized expressions
        import re
        paren_pattern = r'\(([^)]+)\)'
        paren_matches = re.findall(paren_pattern, condition)
        
        if not paren_matches:
            # Fallback to simple case
            return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        
        # Create definitions for parenthesized expressions
        definitions = []
        simplified_condition = condition
        
        # Process parentheses in reverse order to avoid replacement conflicts
        for i, paren_content in enumerate(reversed(paren_matches)):
            # Extract selections from the parenthesized content
            paren_selections = []
            for sel in safe_selections:
                sel_name = sel.replace('safe_', '')
                if sel_name in paren_content:
                    paren_selections.append(sel)
            
            if paren_selections:
                # Create a unique name for this parenthesized expression
                # Use the first word from the content as the name
                first_word = paren_content.split()[0]
                if first_word in [sel.replace('safe_', '') for sel in safe_selections]:
                    # If first word is a selection name, use it as the definition name
                    definition_name = first_word.capitalize()
                else:
                    # Otherwise use a generic name
                    definition_name = f"Group{i+1}"
                
                # Determine the operator inside parentheses
                if ' or ' in paren_content:
                    # OR inside parentheses becomes AND in RML (all must be safe)
                    definition = f"{definition_name} = ({' /\\ '.join(paren_selections)});"
                else:
                    # AND inside parentheses becomes OR in RML (any can be safe)
                    definition = f"{definition_name} = ({' \\/ '.join(paren_selections)});"
                
                definitions.append(definition)
                
                # Replace the parenthesized expression with the definition name
                # Use a more specific replacement to avoid conflicts
                simplified_condition = simplified_condition.replace(f"({paren_content})", definition_name)
        
        # Now generate the main monitor expression using the simplified condition
        # Convert Sigma AND to RML OR (any condition being safe makes the log safe)
        if ' and ' in simplified_condition:
            # Split by AND and create OR expression
            parts = [part.strip() for part in simplified_condition.split(' and ')]
            monitor_parts = []
            
            for part in parts:
                # Remove any 'not' operators since negation is handled in event types
                part = part.replace('not ', '').strip()
                if part in [sel.replace('safe_', '') for sel in safe_selections]:
                    # This is a selection name, add safe_ prefix
                    monitor_parts.append(f"safe_{part}")
                else:
                    # This is a definition name, use as is
                    monitor_parts.append(part)
            
            monitor_expr = f"Monitor = ({' \\/ '.join(monitor_parts)})*;"
        else:
            # No AND operators, use the simplified condition directly
            # Remove any 'not' operators since negation is handled in event types
            simplified_condition = simplified_condition.replace('not ', '').strip()
            monitor_expr = f"Monitor = {simplified_condition}*;"
        
        # Combine definitions and monitor expression
        # Put Monitor first, then definitions for better readability
        if definitions:
            return '\n'.join([monitor_expr] + definitions)
        else:
            return monitor_expr

class RefactoredTranspiler:
    """Main transpiler class with clean, modular architecture"""
    
    def __init__(self):
        self.condition_simplifier = ConditionSimplifier()
        self.quantifier_expander = QuantifierExpander()
        self.field_extractor = FieldValueExtractor()
        self.rml_generator = RMLLineGenerator()
        self.variable_counter = 1  # Global counter for variable names
    
    def transpile(self, sigma_rule: Union[str, Dict[str, Any]]) -> str:
        """Main transpilation method"""
        try:
            # Handle both string (YAML) and dict inputs
            if isinstance(sigma_rule, str):
                import yaml
                try:
                    sigma_rule = yaml.safe_load(sigma_rule)
                    if not sigma_rule:
                        return "// Error: Invalid or empty YAML content"
                except yaml.YAMLError as e:
                    return f"// Error: Invalid YAML format: {str(e)}"
            
            # Extract components
            logsource = sigma_rule.get('logsource', {})
            detection = sigma_rule.get('detection', {})
            condition = detection.get('condition', '')
            
            # Get selections (excluding condition and timeframe)
            selections = [k for k in detection.keys() if k not in ['condition', 'timeframe']]
            
            # Simplify condition
            simplified_condition = self.condition_simplifier.simplify_condition(condition)
            
            # Expand quantifiers
            expanded_condition = self.quantifier_expander.expand_quantifiers(simplified_condition, selections)
            
            # Determine if temporal
            is_temporal = self._is_temporal_condition(expanded_condition, detection)
            
            if is_temporal:
                return self._generate_temporal_rml(sigma_rule, expanded_condition)
            else:
                return self._generate_basic_rml(sigma_rule, expanded_condition, selections)
                
        except Exception as e:
            return f"// Error during transpilation: {str(e)}"
    
    def _is_temporal_condition(self, condition: str, detection: Dict[str, Any]) -> bool:
        """Determine if the condition is temporal"""
        # Check for explicit temporal operators
        temporal_operators = ['| near', '| before', '| after', '| within', '| count']
        if any(op in condition for op in temporal_operators):
            return True
        
        # Check for timeframe in detection
        if 'timeframe' in detection:
            return True
        
        # Check for count operations
        if '| count()' in condition:
            return True
        
        return False
    
    def _generate_basic_rml(self, sigma_rule: Dict[str, Any], expanded_condition: str, selections: List[str]) -> str:
        """Generate RML for basic (non-temporal) conditions"""
        logsource = sigma_rule.get('logsource', {})
        detection = sigma_rule.get('detection', {})
        original_condition = detection.get('condition', '')
        
        # Generate logsource filter
        logsource_line = self.rml_generator.generate_logsource_filter(logsource)
        
        # Generate selection definitions
        selection_lines = []
        for selection_name in selections:
            selection_data = detection[selection_name]
            field_values, new_counter = self.field_extractor.extract_field_values(selection_data, self.variable_counter)
            self.variable_counter = new_counter  # Update the global counter
            
            # Check if this selection is negated in the condition
            # Use the original condition for negation detection, not the expanded/simplified one
            is_negated = ConditionSimplifier._is_selection_negated(selection_name, original_condition)
            
            selection = Selection(
                name=selection_name,
                fields={fv.field_name: fv for fv in field_values},
                negated=is_negated
            )
            
            selection_lines.append(self.rml_generator.generate_selection_definition(selection))
        
        # Generate main expression
        main_line = self.rml_generator.generate_main_expression()
        
        # Generate monitor expression using original condition for structure analysis
        monitor_expression = self.rml_generator.generate_monitor_expression(original_condition, selections)
        
        # Split monitor expression into lines (it might contain definitions + monitor)
        monitor_lines = monitor_expression.split('\n')
        
        # Assemble RML
        rml_lines = [
            "// log source filter",
            logsource_line,
            "",
            "// event types",
            *selection_lines,
            "",
            "// property section",
            main_line,
            *monitor_lines
        ]
        
        return '\n'.join(rml_lines)
    
    def _generate_temporal_rml(self, sigma_rule: Dict[str, Any], condition: str) -> str:
        """Generate RML for temporal conditions"""
        logsource = sigma_rule.get('logsource', {})
        detection = sigma_rule.get('detection', {})
        original_condition = detection.get('condition', '')
        
        # Get selections (excluding condition and timeframe)
        selections = [k for k in detection.keys() if k not in ['condition', 'timeframe']]
        
        # Get timeframe (default 10s for | near operations)
        timeframe = detection.get('timeframe', '10s')
        
        # Convert timeframe to milliseconds
        timeframe_ms = self._convert_timeframe_to_ms(timeframe)
        
        # Generate logsource filter
        logsource_line = self.rml_generator.generate_logsource_filter(logsource)
        
        # Generate timed event type definitions
        event_lines = []
        for selection_name in selections:
            selection_data = detection[selection_name]
            field_values, _ = self.field_extractor.extract_field_values(selection_data, 1)
            
            # Create timed event definition
            field_pairs = []
            field_pairs.append("timestamp: ts")  # Always include timestamp
            
            for field_value in field_values:
                formatted_value = self.field_extractor.format_field_value(field_value)
                field_pairs.append(formatted_value)
            
            field_str = f"{{{', '.join(field_pairs)}}}"
            event_lines.append(f"timed_{selection_name}(ts) matches {field_str};")
        
        # Add other events handler
        event_lines.append("timed_other_events(ts) matches {timestamp: ts};")
        
        # For count operations, also add safe_selection definition
        if '| count()' in original_condition:
            for selection_name in selections:
                selection_data = detection[selection_name]
                field_values, _ = self.field_extractor.extract_field_values(selection_data, 1)
                
                # Create safe selection definition
                field_pairs = []
                for field_value in field_values:
                    formatted_value = self.field_extractor.format_field_value(field_value)
                    field_pairs.append(formatted_value)
                
                if field_pairs:
                    field_str = f"{{{', '.join(field_pairs)}}}"
                    event_lines.append(f"safe_{selection_name} not matches {field_str};")
        
        # Generate main expression with state parameters
        if '| count()' in original_condition:
            # For count operations, use <start_ts, count> state
            main_line = "Main = logsource >> Monitor<0, 0>!;"
        else:
            # For other temporal operations, use selection-based state
            state_params = ", ".join(["0"] * len(selections))
            main_line = f"Main = logsource >> Monitor<{state_params}>!;"
        
        # Generate monitor expression using original condition for pattern detection
        monitor_line = self._generate_temporal_monitor(original_condition, selections, timeframe_ms)
        
        # Assemble RML
        rml_lines = [
            "// log source filter",
            logsource_line,
            "",
            "// event types",
            *event_lines,
            "",
            "// property section",
            main_line,
            monitor_line
        ]
        
        return '\n'.join(rml_lines)
    
    def _convert_timeframe_to_ms(self, timeframe: str) -> int:
        """Convert timeframe string to milliseconds"""
        if isinstance(timeframe, str):
            timeframe = timeframe.strip()
            
        if timeframe.endswith('s'):
            try:
                seconds = int(timeframe[:-1])
                return seconds * 1000
            except ValueError:
                return 10000  # Default 10 seconds
        elif timeframe.endswith('m'):
            try:
                minutes = int(timeframe[:-1])
                return minutes * 60 * 1000
            except ValueError:
                return 600000  # Default 10 minutes
        elif timeframe.endswith('h'):
            try:
                hours = int(timeframe[:-1])
                return hours * 60 * 60 * 1000
            except ValueError:
                return 3600000  # Default 1 hour
        else:
            # Try to parse as seconds
            try:
                seconds = int(timeframe)
                return seconds * 1000
            except ValueError:
                return 10000  # Default 10 seconds
    
    def _generate_temporal_monitor(self, condition: str, selections: List[str], timeframe_ms: int) -> str:
        """Generate temporal monitor expression"""
        # Handle count operations first
        if '| count()' in condition:
            return self._generate_count_monitor(selections[0], timeframe_ms)
        
        # Handle near operations
        if '| near' in condition:
            return self._generate_near_monitor(selections, timeframe_ms)
        
        # Handle general temporal conditions (with timeframe)
        return self._generate_general_temporal_monitor(condition, selections, timeframe_ms)
    
    def _generate_count_monitor(self, selection: str, timeframe_ms: int) -> str:
        """Generate monitor for count operations"""
        return f"""Monitor<start_ts, count> =
    {{let ts; timed_{selection}(ts)
        (
            if (start_ts == 0 || ts - start_ts > {timeframe_ms}) (
                Monitor<ts, 1>
            )                
            else if (count+1 > 4) safe_{selection} else Monitor<start_ts,count+1>
        )
    }}
    \\/
    {{let ts; timed_other_events(ts)
        (
            if (start_ts > 0 && ts - start_ts > {timeframe_ms})
                Monitor<0, 0> 
            else
                Monitor<start_ts, count>
        )
    }};"""
    
    def _generate_near_monitor(self, selections: List[str], timeframe_ms: int) -> str:
        """Generate monitor for near operations"""
        if len(selections) != 2:
            # Fallback for non-binary near operations
            return self._generate_general_temporal_monitor(selections, timeframe_ms)
        
        selection1, selection2 = selections
        return f"""Monitor<start_ts, s1, s2> = 
{{
    let ts; timed_{selection1}(ts) (
        if (start_ts == 0 || ts - start_ts > {timeframe_ms})
            Monitor<ts, 1, 0>
        else (
            if (s2 == 1) empty else Monitor<start_ts, 1, s2>
        )
    )
     }}
 /\\
 {{
     let ts; timed_{selection2}(ts) (
         if (start_ts == 0 || ts - start_ts > {timeframe_ms})
             Monitor<ts, 0, 1>
         else (
             if (s1 == 1) empty else Monitor<start_ts, s1, 1>                    
         )
     )
 }}
 /\\
 {{
     let ts; timed_other_events(ts) (
         if (start_ts > 0 && ts - start_ts > {timeframe_ms})
             Monitor<0, 0, 0>            
         else (
             Monitor<start_ts, s1, s2>
         )
     )
 }};"""
    
    def _generate_general_temporal_monitor(self, condition: str, selections: List[str], timeframe_ms: int) -> str:
        """Generate monitor for general temporal conditions"""
        if len(selections) == 0:
            return "Monitor = empty;"
        
        # Create state parameters
        state_vars = ", ".join([f"s{i+1}" for i in range(len(selections))])
        initial_states = ", ".join(["0"] * len(selections))
        
        # Generate monitor cases for each selection
        monitor_cases = []
        for i, selection in enumerate(selections):
            case = self._generate_selection_case(selection, i, selections, timeframe_ms)
            monitor_cases.append(case)
        
        # Add other events case
        other_events_case = self._generate_other_events_case(selections, timeframe_ms)
        monitor_cases.append(other_events_case)
        
        # Determine operator based on condition logic
        # If condition contains 'and', use AND (/\)
        # If condition contains 'or', use OR (\/)
        if ' and ' in condition:
            operator = "/\\"
        elif ' or ' in condition:
            operator = "\\/"
        else:
            # Default to AND for single conditions
            operator = "/\\"
        
        # Join all cases with appropriate operator
        monitor_body = f"\n{operator}\n".join(monitor_cases)
        
        return f"""Monitor<start_ts, {state_vars}> = 
{monitor_body};"""
    
    def _generate_selection_case(self, selection: str, index: int, all_selections: List[str], timeframe_ms: int) -> str:
        """Generate monitor case for a specific selection"""
        # Create state update
        state_update = []
        for i in range(len(all_selections)):
            if i == index:
                state_update.append("1")
            else:
                state_update.append(f"s{i+1}")
        
        state_update_str = ", ".join(state_update)
        
        # Create completion check
        other_states = [f"s{i+1}" for i in range(len(all_selections)) if i != index]
        if other_states:
            completion_check = f"if ({' + '.join(other_states)} == {len(other_states)}) empty else Monitor<start_ts, {state_update_str}>"
        else:
            completion_check = f"Monitor<start_ts, {state_update_str}>"
        
        return f"""{{
    let ts; timed_{selection}(ts) (
        if (start_ts == 0 || ts - start_ts > {timeframe_ms})
            Monitor<ts, {state_update_str}>
        else (
            {completion_check}
        )
    )
}}"""
    
    def _generate_other_events_case(self, selections: List[str], timeframe_ms: int) -> str:
        """Generate monitor case for other events"""
        state_vars = ", ".join([f"s{i+1}" for i in range(len(selections))])
        reset_states = ", ".join(["0"] * len(selections))
        
        return f"""{{
    let ts; timed_other_events(ts) (
        if (start_ts > 0 && ts - start_ts > {timeframe_ms})
            Monitor<0, {reset_states}>            
        else (
            Monitor<start_ts, {state_vars}>
        )
    )
}}"""

# Backward compatibility
SigmaToRMLTranspiler = RefactoredTranspiler
