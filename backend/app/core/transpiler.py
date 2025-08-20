# backend/app/core/transpiler.py

from .ast.nodes import ASTNode
from .parser import SigmaParser

class SigmaToRMLTranspiler:
    def __init__(self):
        self.parser = SigmaParser()

    def transpile(self, yaml_input):
        """
        Main transpilation method that converts Sigma YAML to RML
        Accepts either a YAML string or a parsed dictionary
        Now produces the correct RML format as shown in the examples
        """
        try:
            # Handle both string and dictionary inputs
            if isinstance(yaml_input, str):
                ast = self.parser.parse(yaml_input)
            elif isinstance(yaml_input, dict):
                # If it's already a dictionary, parse it directly
                ast = self.parser.parse_dict(yaml_input)
            else:
                raise ValueError(f"Expected string or dict, got {type(yaml_input)}")
            
            lines = []
            
            # 1. Logsource (if present)
            if ast['logsource']:
                lines.append(ast['logsource'].to_rml())
                lines.append("")
            
            # 2. Event types (selections)
            for match_node in ast['matches']:
                lines.append(match_node.to_rml())
                
                # Add comparison constraints if any
                if hasattr(match_node, 'get_comparison_constraints'):
                    constraints = match_node.get_comparison_constraints()
                    for constraint in constraints:
                        lines.append(f"// {constraint}")
            
            # 3. Safe/No event types (negations) - use new negation approach
            for match_node in ast['matches']:
                # Use the new negation method that generates "not matches" with opposite conditions
                lines.append(match_node.get_negation_rml())
            
            lines.append("")
            
            # 4. Property section
            if ast['main']:
                main_expr = ast['main'].to_rml()
                
                # Handle different main expression patterns
                if ast['logsource']:
                    if self._is_temporal_expression(ast['main']):
                        # For temporal expressions, we need special handling
                        lines.append(f"Main = logsource >> Monitor!;")
                        lines.append(self._generate_temporal_monitor(ast))
                    else:
                        # Most conditions use Monitor! according to the examples
                        lines.append(f"Main = logsource >> Monitor!;")
                        lines.append(self._generate_monitor_expression(ast))
                else:
                    if self._is_temporal_expression(ast['main']):
                        lines.append(f"Main = Monitor!;")
                        lines.append(self._generate_temporal_monitor(ast))
                    else:
                        lines.append(f"Main = Monitor!;")
                        lines.append(self._generate_monitor_expression(ast))
            else:
                lines.append("// Translation not supported: Main expression not available")
            
            return "\n".join(lines)
            
        except Exception as e:
            # Provide more detailed error information
            error_msg = f"Transpilation failed: {str(e)}"
            if "condition" in str(e).lower():
                error_msg += "\n// Tip: Check your condition syntax and supported operators"
            elif "selection" in str(e).lower():
                error_msg += "\n// Tip: Verify your selection names and field definitions"
            elif "temporal" in str(e).lower():
                error_msg += "\n// Tip: Check temporal operator syntax (e.g., 'selection1 | near selection2')"
            
            return f"// ERROR: {error_msg}"

    def _is_temporal_expression(self, expr) -> bool:
        """
        Check if the expression contains temporal operators
        """
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
        if not ast['matches']:
            return "Monitor = empty;"
        
        # Check if the main expression contains quantifiers
        main_expr = ast['main'].to_rml() if ast['main'] else ""
        
        # Check the quantifier type by examining the original condition and AST node
        condition_str = self._get_condition_string(ast)
        
        if "1 of" in condition_str.lower() or (hasattr(ast['main'], 'quantifier') and "1 of" in ast['main'].quantifier):
            # For "1 of" patterns, use safe_ prefix and AND in Monitor
            safe_selections = []
            for match_node in ast['matches']:
                safe_name = f"safe_{match_node.name}" if hasattr(match_node, 'name') else "safe_selection"
                safe_selections.append(safe_name)
            
            if len(safe_selections) == 1:
                return f"Monitor = {safe_selections[0]}*;"
            else:
                return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
        elif "all of" in condition_str.lower() or (hasattr(ast['main'], 'quantifier') and "all of" in ast['main'].quantifier):
            # For "all of" patterns, use safe_ prefix and OR in Monitor
            safe_selections = []
            for match_node in ast['matches']:
                safe_name = f"safe_{match_node.name}" if hasattr(match_node, 'name') else "safe_selection"
                safe_selections.append(safe_name)
            
            if len(safe_selections) == 1:
                return f"Monitor = {safe_selections[0]}*;"
            else:
                return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
        else:
            # For regular conditions, check the actual logical structure
            # Get the condition string from the original input to determine AND vs OR
            condition_str = self._get_condition_string(ast)
            
            if " and " in condition_str.lower():
                # Sigma AND condition: use OR in RML Monitor (negative logic)
                safe_selections = []
                for match_node in ast['matches']:
                    safe_name = f"safe_{match_node.name}" if hasattr(match_node, 'name') else "safe_selection"
                    safe_selections.append(safe_name)
                
                if len(safe_selections) == 1:
                    return f"Monitor = {safe_selections[0]}*;"
                else:
                    return f"Monitor = ({' \\/ '.join(safe_selections)})*;"
            elif " or " in condition_str.lower():
                # Sigma OR condition: use AND in RML Monitor (negative logic)
                safe_selections = []
                for match_node in ast['matches']:
                    safe_name = f"safe_{match_node.name}" if hasattr(match_node, 'name') else "safe_selection"
                    safe_selections.append(safe_name)
                
                if len(safe_selections) == 1:
                    return f"Monitor = {safe_selections[0]}*;"
                else:
                    return f"Monitor = ({' /\\ '.join(safe_selections)})*;"
            else:
                # Single selection: use single safe selection
                safe_selections = []
                for match_node in ast['matches']:
                    safe_name = f"safe_{match_node.name}" if hasattr(match_node, 'name') else "safe_selection"
                    safe_selections.append(safe_name)
                
                if len(safe_selections) == 1:
                    return f"Monitor = {safe_selections[0]}*;"
                else:
                    # Default to OR for multiple selections without explicit operators
                    return f"Monitor = ({' \\/ '.join(safe_selections)})*;"

    def _generate_temporal_monitor(self, ast):
        """
        Generate the Monitor expression for temporal rules
        """
        if not ast['main']:
            return "Monitor = empty;"
        
        # Check the type of temporal expression
        if hasattr(ast['main'], 'operator'):
            operator = ast['main'].operator
            
            if operator == 'near':
                # selection1 | near selection2
                selection1 = ast['main'].selection1
                selection2 = ast['main'].selection2
                timeframe = ast['main'].timeframe or "10s"  # Default 10 seconds
                
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
                selection = ast['main'].selection1
                count_expr = ast['main'].count or "5"  # Default threshold
                timeframe = ast['main'].timeframe or "1m"  # Default 1 minute for count operations
                
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
    
    def _convert_timeframe_to_ms(self, timeframe: str) -> str:
        """
        Convert timeframe string to milliseconds for RML
        Supports: s (seconds), m (minutes), h (hours), d (days)
        Examples: 10s -> 10000ms, 5m -> 300000ms, 1h -> 3600000ms, 2d -> 172800000ms
        """
        if not timeframe:
            return "10000"  # Default 10 seconds
        
        timeframe = timeframe.lower().strip()
        
        try:
            if timeframe.endswith('s'):
                # Seconds: 10s -> 10000ms
                seconds = int(timeframe[:-1])
                return str(seconds * 1000)
            elif timeframe.endswith('m'):
                # Minutes: 5m -> 300000ms
                minutes = int(timeframe[:-1])
                return str(minutes * 60 * 1000)
            elif timeframe.endswith('h'):
                # Hours: 1h -> 3600000ms
                hours = int(timeframe[:-1])
                return str(hours * 60 * 60 * 1000)
            elif timeframe.endswith('d'):
                # Days: 2d -> 172800000ms
                days = int(timeframe[:-1])
                return str(days * 24 * 60 * 60 * 1000)
            else:
                # Assume seconds if no unit specified
                seconds = int(timeframe)
                return str(seconds * 1000)
        except (ValueError, IndexError):
            return "10000"  # Default 10 seconds on error

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

    def _get_condition_string(self, ast):
        """
        Extract the original condition string from the AST
        """
        # Get the stored original condition string
        if 'original_condition' in ast:
            return ast['original_condition']
        
        # Fallback: try to get from main expression
        if ast['main'] and hasattr(ast['main'], 'to_rml'):
            return ast['main'].to_rml()
        
        # Fallback: reconstruct from available names
        if ast['matches']:
            names = [match.name for match in ast['matches'] if hasattr(match, 'name')]
            if len(names) > 1:
                return " and ".join(names)  # Default to AND for multiple selections
            elif len(names) == 1:
                return names[0]
        
        return ""
