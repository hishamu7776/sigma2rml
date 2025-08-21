# backend/app/core/transpiler.py

import yaml
import re
from .ast.condition_parser import ConditionParser
from .ast.nodes import ASTNode, MatchNode, NameNode, AndNode, OrNode, NotNode, UnsupportedNode, QuantifierNode, TemporalNode
from .ast.temporal_monitor import EnhancedTemporalNode

class SigmaToRMLTranspiler:
    """
    Transpiles Sigma rules to Runtime Monitoring Language (RML)
    """
    
    def __init__(self):
        self.supported_products = ['windows', 'linux', 'macos', 'unix']
        self.supported_services = ['security', 'sysmon', 'auditd', 'system']
        self.supported_modifiers = ['lt', 'lte', 'gt', 'gte', 'contains', 'startswith', 'endswith', 're', 'base64', 'base64offset', 'wide', 'all', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    def transpile(self, sigma_input):
        """
        Main transpilation method
        Args:
            sigma_input: Sigma rule as string or dict
        Returns:
            RML string
        """
        try:
            # Parse input
            if isinstance(sigma_input, str):
                sigma_dict = yaml.safe_load(sigma_input)
            else:
                sigma_dict = sigma_input
            
            if not sigma_dict:
                return "// ERROR: Invalid or empty Sigma rule"
            
            # Extract components
            logsource = sigma_dict.get('logsource', {})
            detection = sigma_dict.get('detection', {})
            condition = detection.get('condition', 'selection') if detection else 'selection'
            
            # Store the original condition string for later use
            self.original_condition = condition
            
            # Check if this is a temporal condition by looking for temporal operators in the condition
            # NOT just by the presence of timeframe field
            is_temporal = self._has_temporal_operators(condition)
            
            # Parse condition
            available_names = list(detection.keys()) if detection else []
            available_names = [name for name in available_names if name != 'condition' and name != 'timeframe']
            
            parser = ConditionParser(available_names, detection)
            
            # Only use temporal parsing if the condition actually contains temporal operators
            if is_temporal:
                # Add timeframe to the condition string so the parser can detect it
                timeframe = detection.get('timeframe', '5m')
                condition_with_timeframe = f"{condition} timeframe:{timeframe}"
                ast = parser.parse(condition_with_timeframe)
            else:
                ast = parser.parse(condition)
            
            # Build RML
            rml_parts = []
            
            # Add logsource filter
            if logsource:
                rml_parts.append(self._generate_logsource_filter(logsource))
            else:
                # Provide default logsource if none specified
                rml_parts.append("// log source filter")
                rml_parts.append("logsource matches {product: 'windows', service: 'security'};")
            
            # Add selection definitions
            rml_parts.append("// event types")
            rml_parts.append(self._generate_selection_definitions(detection))
            
            # Add main expression
            if ast:
                rml_parts.append("// property section")
                rml_parts.append(self._generate_main_expression(ast, detection))
            
            # Add monitor expression
            if self._is_temporal_expression(ast):
                rml_parts.append(self._generate_temporal_monitor(ast))
            else:
                rml_parts.append(self._generate_monitor_expression(ast))
            
            return '\n\n'.join(rml_parts)
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages
            if "yaml" in error_msg.lower():
                error_msg += "\n// Tip: Check your YAML syntax"
            elif "condition" in error_msg.lower():
                error_msg += "\n// Tip: Check your condition syntax and supported operators"
            elif "selection" in error_msg.lower():
                error_msg += "\n// Tip: Verify your selection names and field definitions"
            elif "temporal" in error_msg.lower():
                error_msg += "\n// Tip: Check temporal operator syntax (e.g., 'selection1 | near selection2')"
            
            return f"// ERROR: {error_msg}"

    def _is_temporal_expression(self, expr) -> bool:
        """
        Check if the expression contains temporal operators
        """
        # Check if the main expression is an EnhancedTemporalNode
        if isinstance(expr, EnhancedTemporalNode):
            return True
        
        # Check if the main expression is a TemporalNode
        if hasattr(expr, '__class__') and 'TemporalNode' in str(expr.__class__):
            return True
        
        # Check string indicators
        temporal_indicators = ['temporal_near', 'temporal_before', 'temporal_after', 'temporal_within', '| near', '| count']
        return any(indicator in str(expr) for indicator in temporal_indicators)

    def _generate_monitor_expression(self, ast):
        """
        Generate the Monitor expression for non-temporal rules
        """
        if not ast:
            return "Monitor = empty;"
        
        # For temporal conditions, this should not be called
        if isinstance(ast, EnhancedTemporalNode):
            return "// Monitor handled by temporal monitor"
        
        # Get the condition string to determine the logical structure
        condition_str = self._get_condition_string(ast)
        
        # Extract selection names from the AST
        selections = self._extract_selections_from_ast(ast)
        
        if not selections:
            return "Monitor = empty;"
        
        # Generate safe selection names
        safe_selections = [f"safe_{selection}" for selection in selections]
        
        # Determine the logical structure based on the condition
        if "1 of" in condition_str.lower():
            # For "1 of" patterns, use AND in Monitor (negative logic)
            if len(safe_selections) == 1:
                return f"Monitor = {safe_selections[0]}*;"
            else:
                return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        elif "all of" in condition_str.lower():
            # For "all of" patterns, use OR in Monitor (negative logic)
            if len(safe_selections) == 1:
                return f"Monitor = {safe_selections[0]}*;"
            else:
                return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
        elif "any of" in condition_str.lower():
            # For "any of" patterns, use AND in Monitor (negative logic)
            if len(safe_selections) == 1:
                return f"Monitor = {safe_selections[0]}*;"
            else:
                return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        elif re.search(r'\b\d+ of\b', condition_str.lower()):
            # Check if it's a supported number
            match = re.search(r'\b(\d+) of\b', condition_str.lower())
            if match:
                number = int(match.group(1))
                if number == 1:
                    # 1 of is supported
                    if len(safe_selections) == 1:
                        return f"Monitor = {safe_selections[0]}*;"
                    else:
                        return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
                else:
                    # Other numbers are not supported
                    return f"// UNSUPPORTED: {number} of pattern not supported. Only 1 of, any of, all of are supported."
        elif " and " in condition_str.lower():
            # Sigma AND condition: use OR in RML Monitor (negative logic)
            if len(safe_selections) == 1:
                return f"Monitor = {safe_selections[0]}*;"
            else:
                return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
        elif " or " in condition_str.lower():
            # Sigma OR condition: use AND in RML Monitor (negative logic)
            if len(safe_selections) == 1:
                return f"Monitor = {safe_selections[0]}*;"
            else:
                return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        else:
            # Single selection or default case
            if len(safe_selections) == 1:
                return f"Monitor = {safe_selections[0]}*;"
            else:
                # Default to OR for multiple selections without explicit operators
                return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
    
    def _extract_selections_from_ast(self, ast):
        """Extract selection names from the AST, excluding negated ones"""
        selections = set()
        
        if isinstance(ast, NameNode):
            selections.add(ast.name)
        elif isinstance(ast, AndNode):
            selections.update(self._extract_selections_from_ast(ast.left))
            selections.update(self._extract_selections_from_ast(ast.right))
        elif isinstance(ast, OrNode):
            selections.update(self._extract_selections_from_ast(ast.left))
            selections.update(self._extract_selections_from_ast(ast.right))
        elif isinstance(ast, NotNode):
            # For NOT nodes, we don't add the negated selection to the Monitor
            # The negated selection will be handled in the safe_selection definition
            pass
        elif isinstance(ast, QuantifierNode):
            selections.update(ast.selections)
        
        # Filter out negated selections from the Monitor
        condition_str = getattr(self, 'original_condition', '')
        negated_selections = self._extract_negated_selections(condition_str)
        selections = selections - negated_selections
        
        return list(selections)

    def _generate_temporal_monitor(self, ast):
        """
        Generate the Monitor expression for temporal rules
        """
        if not ast:
            return "Monitor = empty;"
        
        # Handle EnhancedTemporalNode
        if isinstance(ast, EnhancedTemporalNode):
            return ast.to_rml()
        
        # Check the type of temporal expression
        if hasattr(ast, 'operator'):
            operator = ast.operator
            
            if operator == 'near':
                # selection1 | near selection2
                selection1 = ast.selection1
                selection2 = ast.selection2
                # For near operations, use 10s default if no timeframe specified
                if hasattr(ast, 'timeframe') and ast.timeframe:
                    timeframe = ast.timeframe
                else:
                    timeframe = "10s"  # Default 10 seconds for near operations
                
                return f"""Monitor<start_ts, s1, s2> = 
{{
    let ts; {selection1}(ts) (
        if (start_ts == 0 || ts - start_ts > {self._convert_timeframe_to_ms(timeframe)})
            Monitor<ts, 1, 0>
        else (
            if (s2 == 1) empty else Monitor<start_ts, 1, s2>
        )
    )
}}
\\/
{{
    let ts; {selection2}(ts) (
        if (start_ts == 0 || ts - start_ts > {self._convert_timeframe_to_ms(timeframe)})
            Monitor<ts, 0, 1>
        else (
            if (s1 == 1) empty else Monitor<start_ts, s1, 1>                   
        )
    )
}}
\\/
{{
    let ts; other_events(ts) (
        if (start_ts > 0 && ts - start_ts > {self._convert_timeframe_to_ms(timeframe)})
            Monitor<0, 0, 0>           
        else (
            Monitor<start_ts, s1, s2>
        )
    )
}};"""
            
            elif operator == 'count':
                # selection | count() > N
                selection = ast.selection1
                count_expr = ast.count or "5"  # Default threshold
                timeframe = ast.timeframe or "1m"  # Default 1 minute for count operations
                
                # Extract just the number from the count expression
                count_number = "5"  # Default
                if count_expr and '>' in count_expr:
                    try:
                        number = count_expr.split('>')[-1]
                        if number.isdigit():
                            count_number = number
                    except:
                        pass
                
                return f"""Monitor<start_ts, count> =
    {{let ts; {selection}(ts)
        (
            if (start_ts == 0 || ts - start_ts > {self._convert_timeframe_to_ms(timeframe)}) (
                Monitor<ts, 1>
            )               
            else if (count+1 > {count_number}) safe_{selection} else Monitor<start_ts,count+1>
        )
    }}
    \\/
    {{let ts; other_events(ts)
        (
            if (start_ts > 0 && ts - start_ts > {self._convert_timeframe_to_ms(timeframe)})
                Monitor<0, 0> 
            else
                Monitor<count, start_ts>
        )
    }};"""
            
            else:
                # Other temporal operators
                return f"// TODO: Implement {operator} temporal Monitor expression"
        
        return "// TODO: Implement temporal Monitor expression based on specific operator"
    
    def _generate_logsource_filter(self, logsource: dict) -> str:
        """Generate logsource filter RML"""
        if not logsource:
            return ""
        
        filters = []
        for key, value in logsource.items():
            if isinstance(value, str):
                filters.append(f"{key}: '{value}'")
            else:
                filters.append(f"{key}: {value}")
        
        if filters:
            return f"logsource matches {{{', '.join(filters)}}};"
        return ""
    
    def _generate_selection_definitions(self, detection: dict) -> str:
        """Generate selection definitions RML"""
        if not detection:
            return ""
        
        rml_lines = []
        
        for key, value in detection.items():
            if key in ['condition', 'timeframe']:
                continue
                
            if isinstance(value, dict):
                # Handle field-based selections
                field_pairs = []
                for field, field_value in value.items():
                    if isinstance(field_value, list):
                        # Handle list values
                        if all(isinstance(v, str) for v in field_value):
                            quoted_values = [f"'{v}'" for v in field_value]
                            field_pairs.append(f"{field.lower()}: {' | '.join(quoted_values)}")
                        else:
                            field_pairs.append(f"{field.lower()}: {' | '.join(str(v) for v in field_value)}")
                    elif isinstance(field_value, str):
                        field_pairs.append(f"{field.lower()}: '{field_value}'")
                    else:
                        field_pairs.append(f"{field.lower()}: {field_value}")
                
                if field_pairs:
                    rml_lines.append(f"{key} matches {{{', '.join(field_pairs)}}};")
                else:
                    rml_lines.append(f"{key} matches {{}};")
            else:
                # Handle simple selections
                rml_lines.append(f"{key} matches {{}};")
        
        # Add negation definitions for safe selections
        # We need to analyze the condition to determine which selections are negated
        condition_str = getattr(self, 'original_condition', '')
        negated_selections = self._extract_negated_selections(condition_str)
        
        for key in detection.keys():
            if key not in ['condition', 'timeframe']:
                if key in negated_selections:
                    # This selection is negated, so safe_selection should match the selection
                    rml_lines.append(f"safe_{key} matches {key};")
                else:
                    # This selection is not negated, so safe_selection should not match the selection
                    rml_lines.append(f"safe_{key} not matches {key};")
        
        # Add comment for negation section
        if rml_lines:
            rml_lines.insert(0, "// negation")
        
        return "\n".join(rml_lines)
    
    def _extract_negated_selections(self, condition_str: str) -> set:
        """Extract which selections are negated in the condition"""
        negated = set()
        if not condition_str:
            return negated
        
        # Simple pattern matching for NOT conditions
        # Look for patterns like "not selection" or "~selection"
        import re
        
        # Pattern 1: "not selection" (space separated)
        not_pattern1 = r'\bnot\s+(\w+)'
        matches1 = re.findall(not_pattern1, condition_str.lower())
        negated.update(matches1)
        
        # Pattern 2: "~selection" (tilde prefix)
        not_pattern2 = r'~(\w+)'
        matches2 = re.findall(not_pattern2, condition_str.lower())
        negated.update(matches2)
        
        return negated
    
    def _generate_main_expression(self, ast: ASTNode, detection: dict) -> str:
        """Generate main expression RML"""
        if not ast:
            return ""
        
        # For temporal conditions, the main expression is handled by the temporal monitor
        if isinstance(ast, EnhancedTemporalNode):
            return "// Main expression handled by temporal monitor"
        
        # For basic patterns, always generate the Main line
        # Don't call ast.to_rml() as it generates AST representation instead of Main line
        if isinstance(ast, NameNode):
            # Single selection
            return f"Main = logsource >> Monitor;"
        elif isinstance(ast, AndNode):
            # AND condition
            return f"Main = logsource >> Monitor;"
        elif isinstance(ast, OrNode):
            # OR condition
            return f"Main = logsource >> Monitor;"
        elif isinstance(ast, NotNode):
            # NOT condition
            return f"Main = logsource >> Monitor;"
        elif isinstance(ast, QuantifierNode):
            # Quantifier condition - this is a basic pattern, not temporal
            return f"Main = logsource >> Monitor;"
        
        # Fallback for any other node types
        return f"Main = logsource >> Monitor;"
    
    def _get_node_representation(self, node) -> str:
        """Get a string representation of a node"""
        if isinstance(node, NameNode):
            return node.name
        elif isinstance(node, AndNode):
            left = self._get_node_representation(node.left)
            right = self._get_node_representation(node.right)
            return f"({left} and {right})"
        elif isinstance(node, OrNode):
            left = self._get_node_representation(node.left)
            right = self._get_node_representation(node.right)
            return f"({left} or {right})"
        elif isinstance(node, NotNode):
            operand = self._get_node_representation(node.operand)
            return f"not {operand}"
        elif isinstance(node, QuantifierNode):
            return f"{node.quantifier} of {', '.join(node.selections)}"
        else:
            return str(node)
    
    def _get_condition_string(self, ast) -> str:
        """Get the original condition string for analysis"""
        return getattr(self, 'original_condition', 'selection')
    
    def _convert_timeframe_to_ms(self, timeframe: str) -> str:
        """
        Convert timeframe string to milliseconds for RML
        Supports: s (seconds), m (minutes), h (hours), d (days)
        Examples: 10s -> 10000ms, 5m -> 300000ms, 1h -> 3600000ms, 2d -> 172800000ms
        """
        if not timeframe:
            return "10000"  # Default 10 seconds
        
        timeframe = timeframe.strip().lower()
        
        try:
            if timeframe.endswith('s'):
                seconds = int(timeframe[:-1])
                return str(seconds * 1000)
            elif timeframe.endswith('m'):
                minutes = int(timeframe[:-1])
                return str(minutes * 60 * 1000)
            elif timeframe.endswith('h'):
                hours = int(timeframe[:-1])
                return str(hours * 60 * 60 * 1000)
            elif timeframe.endswith('d'):
                days = int(timeframe[:-1])
                return str(days * 24 * 60 * 60 * 1000)
            else:
                # Assume seconds if no unit specified
                return str(int(timeframe) * 1000)
        except (ValueError, TypeError):
            return "10000"  # Default fallback

    def _format_selection_name(self, name: str) -> str:
        """
        Format selection names consistently
        """
        # Remove any special characters and normalize
        return name.replace(' ', '_').replace('-', '_').lower()

    def _handle_complex_condition(self, condition: str) -> str:
        """
        Handle complex Sigma conditions with better parsing
        """
        # This method can be extended for more complex condition handling
        return condition

    def _has_temporal_operators(self, condition: str) -> bool:
        """
        Check if the condition string contains actual temporal operators
        """
        if not condition:
            return False
        
        # Check for temporal operators
        temporal_operators = ['| near', '| before', '| after', '| within', '| count']
        for op in temporal_operators:
            if op in condition.lower():
                return True
        
        # Quantifiers alone are NOT temporal - they're basic patterns
        # Only treat them as temporal if combined with actual temporal operators
        return False
