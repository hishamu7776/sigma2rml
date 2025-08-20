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
            
            # Check if this is a temporal condition by looking for timeframe
            timeframe = detection.get('timeframe', None)
            is_temporal = timeframe is not None
            
            # Parse condition
            available_names = list(detection.keys()) if detection else []
            available_names = [name for name in available_names if name != 'condition' and name != 'timeframe']
            
            parser = ConditionParser(available_names, detection)
            
            # If we have a timeframe, modify the condition to include it
            if is_temporal:
                # Add timeframe to the condition string so the parser can detect it
                condition_with_timeframe = f"{condition} timeframe:{timeframe}"
                ast = parser.parse(condition_with_timeframe)
            else:
                ast = parser.parse(condition)
            
            # Build RML
            rml_parts = []
            
            # Add logsource filter
            if logsource:
                rml_parts.append(self._generate_logsource_filter(logsource))
            
            # Add selection definitions
            rml_parts.append(self._generate_selection_definitions(detection))
            
            # Add main expression
            if ast:
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
        if not ast or not hasattr(ast, 'matches'):
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
                timeframe = ast.timeframe or "10s"  # Default 10 seconds
                
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
                    rml_lines.append(f"{key}(ts) matches {{{', '.join(field_pairs)}}};")
            else:
                # Handle simple selections
                rml_lines.append(f"{key}(ts) matches {{}};")
        
        return "\n".join(rml_lines)
    
    def _generate_main_expression(self, ast: ASTNode, detection: dict) -> str:
        """Generate main expression RML"""
        if not ast:
            return ""
        
        # For temporal conditions, the main expression is handled by the temporal monitor
        if isinstance(ast, EnhancedTemporalNode):
            return "// Main expression handled by temporal monitor"
        
        # For regular conditions, generate the main expression
        if hasattr(ast, 'to_rml'):
            return ast.to_rml()
        
        return "// Main expression not available"
    
    def _get_condition_string(self, ast) -> str:
        """Get the original condition string for analysis"""
        # This is a placeholder - in a real implementation, you'd need to track the original condition
        return "selection"  # Default fallback
    
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
