"""
Enhanced Temporal Monitor Translation System
Handles complex Sigma temporal conditions with multiple selections, AND/OR operations, and NOT conditions
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from .nodes import ASTNode, NameNode, AndNode, OrNode, NotNode, MatchNode

class TemporalMonitorGenerator:
    """Generates RML temporal monitor patterns for complex Sigma conditions"""
    
    def __init__(self):
        self.timeframe_default = "10s"  # Default timeframe for near operations
        self.timeframe_ms = 10000       # Default in milliseconds (10 seconds)
    
    def parse_timeframe(self, timeframe_str: str) -> int:
        """Parse timeframe string to milliseconds"""
        if not timeframe_str:
            return self.timeframe_ms
        
        # Parse common timeframe formats
        timeframe_str = timeframe_str.strip().lower()
        
        if timeframe_str.endswith('s'):
            try:
                seconds = int(timeframe_str[:-1])
                return seconds * 1000
            except ValueError:
                pass
        elif timeframe_str.endswith('m'):
            try:
                minutes = int(timeframe_str[:-1])
                return minutes * 60 * 1000
            except ValueError:
                pass
        elif timeframe_str.endswith('h'):
            try:
                hours = int(timeframe_str[:-1])
                return hours * 60 * 60 * 1000
            except ValueError:
                pass
        elif timeframe_str.endswith('d'):
            try:
                days = int(timeframe_str[:-1])
                return days * 24 * 60 * 60 * 1000
            except ValueError:
                pass
        
        # Default fallback
        return self.timeframe_ms
    
    def extract_selections_from_condition(self, condition_node: ASTNode) -> List[Tuple[str, bool]]:
        """
        Extract all selections from a condition node with their negation status
        Returns: List of (selection_name, is_negated) tuples
        """
        selections = []
        
        def extract_recursive(node: ASTNode, is_negated: bool = False):
            if isinstance(node, NameNode):
                selections.append((node.name, is_negated))
            elif isinstance(node, NotNode):
                extract_recursive(node.operand, not is_negated)
            elif isinstance(node, AndNode):
                extract_recursive(node.left, is_negated)
                extract_recursive(node.right, is_negated)
            elif isinstance(node, OrNode):
                extract_recursive(node.left, is_negated)
                extract_recursive(node.right, is_negated)
            elif isinstance(node, MatchNode):
                selections.append((node.name, is_negated))
        
        extract_recursive(condition_node)
        return selections
    
    def generate_temporal_monitor(self, selections: List[Tuple[str, bool]], timeframe_ms: int) -> str:
        """
        Generate RML temporal monitor pattern for multiple selections
        Args:
            selections: List of (selection_name, is_negated) tuples
            timeframe_ms: Timeframe in milliseconds
        """
        if not selections:
            return "// No selections found for temporal monitor"
        
        num_selections = len(selections)
        
        # Generate monitor state variables
        state_vars = ", ".join([f"s{i+1}" for i in range(num_selections)])
        initial_state = ", ".join(["0" for _ in range(num_selections)])
        
        # Generate the main monitor declaration
        rml = f"Main = logsource >> Monitor<0, {initial_state}>!;\n"
        rml += f"Monitor<start_ts, {state_vars}> = \n"
        
        # Generate monitor rules for each selection
        for i, (selection_name, is_negated) in enumerate(selections):
            rml += self._generate_selection_rule(selection_name, is_negated, i, num_selections, timeframe_ms)
            if i < num_selections - 1:
                rml += "\n\\/\n"
        
        # Generate other_events rule
        rml += "\n\\/\n"
        rml += self._generate_other_events_rule(num_selections, timeframe_ms)
        
        # Add semicolon at the end
        rml += ";"
        
        return rml
    
    def _generate_selection_rule(self, selection_name: str, is_negated: bool, 
                                selection_index: int, total_selections: int, 
                                timeframe_ms: int) -> str:
        """Generate RML rule for a specific selection"""
        
        # Create safe selection name
        safe_name = f"safe_{selection_name}"
        
        # Generate state update pattern
        new_state = []
        for i in range(total_selections):
            if i == selection_index:
                new_state.append("1")
            else:
                new_state.append(f"s{i+1}")
        
        new_state_str = ", ".join(new_state)
        
        # Generate condition to check if all other selections are satisfied
        other_selections_sum = []
        for i in range(total_selections):
            if i != selection_index:
                other_selections_sum.append(f"s{i+1}")
        
        if other_selections_sum:
            sum_condition = " + ".join(other_selections_sum)
            check_condition = f"if ({sum_condition} == {total_selections - 1}) empty else Monitor<start_ts, {new_state_str}>"
        else:
            check_condition = f"Monitor<start_ts, {new_state_str}>"
        
        # Handle negation - always use (ts) for the selection call
        rml = f"{{\n    let ts; {safe_name}(ts) (\n"
        
        # Generate the main logic
        rml += f"        if (start_ts == 0 || ts - start_ts > {timeframe_ms})\n"
        rml += f"            Monitor<ts, {new_state_str}>\n"
        rml += f"        else (\n"
        rml += f"            {check_condition}\n"
        rml += f"        )\n"
        rml += f"    )\n"
        rml += f"}}"
        
        return rml
    
    def _generate_other_events_rule(self, num_selections: int, timeframe_ms: int) -> str:
        """Generate RML rule for other events (timeout handling)"""
        
        initial_state = ", ".join(["0" for _ in range(num_selections)])
        
        rml = f"{{\n    let ts; other_events(ts) (\n"
        rml += f"        if (start_ts > 0 && ts - start_ts > {timeframe_ms})\n"
        rml += f"            Monitor<0, {initial_state}>\n"
        rml += f"        else (\n"
        rml += f"            Monitor<start_ts, {', '.join([f's{i+1}' for i in range(num_selections)])}>\n"
        rml += f"        )\n"
        rml += f"    )\n"
        rml += f"}}"
        
        return rml
    
    def generate_selection_definitions(self, selections: List[Tuple[str, bool]], detection: dict) -> str:
        """Generate RML definitions for all selections with proper field values"""
        rml_lines = []
        
        for selection_name, is_negated in selections:
            safe_name = f"safe_{selection_name}"
            
            if is_negated:
                # For negated selections, we need to include the actual fields with timestamp
                if selection_name in detection and isinstance(detection[selection_name], dict):
                    field_pairs = ["timestamp: ts"]
                    for field, value in detection[selection_name].items():
                        if isinstance(value, list):
                            # Handle list values
                            if all(isinstance(v, str) for v in value):
                                quoted_values = [f"'{v}'" for v in value]
                                field_pairs.append(f"{field.lower()}: {' | '.join(quoted_values)}")
                            else:
                                field_pairs.append(f"{field.lower()}: {' | '.join(str(v) for v in value)}")
                        elif isinstance(value, str):
                            field_pairs.append(f"{field.lower()}: '{value}'")
                        else:
                            field_pairs.append(f"{field.lower()}: {value}")
                    
                    if field_pairs:
                        rml_lines.append(f"{safe_name}(ts) not matches {{{', '.join(field_pairs)}}};")
                    else:
                        rml_lines.append(f"{safe_name}(ts) not matches {{timestamp: ts}};")
                else:
                    rml_lines.append(f"{safe_name}(ts) not matches {{timestamp: ts}};")
            else:
                # For positive selections, include the actual fields
                if selection_name in detection and isinstance(detection[selection_name], dict):
                    field_pairs = ["timestamp: ts"]
                    for field, value in detection[selection_name].items():
                        if isinstance(value, list):
                            # Handle list values
                            if all(isinstance(v, str) for v in value):
                                quoted_values = [f"'{v}'" for v in value]
                                field_pairs.append(f"{field.lower()}: {' | '.join(quoted_values)}")
                            else:
                                field_pairs.append(f"{field.lower()}: {' | '.join(str(v) for v in value)}")
                        elif isinstance(value, str):
                            field_pairs.append(f"{field.lower()}: '{value}'")
                        else:
                            field_pairs.append(f"{field.lower()}: {value}")
                    
                    rml_lines.append(f"{safe_name}(ts) matches {{{', '.join(field_pairs)}}};")
                else:
                    rml_lines.append(f"{safe_name}(ts) matches {{timestamp: ts}};")
        
        # Add other_events definition
        rml_lines.append("other_events(ts) matches {timestamp: ts};")
        
        return "\n".join(rml_lines)

    def generate_complete_temporal_rml(self, condition_node: ASTNode, timeframe_str: str = None, detection: dict = None) -> str:
        """
        Generate complete RML for temporal monitor
        Args:
            condition_node: The parsed condition AST node
            timeframe_str: Timeframe string (e.g., "5m", "10s")
            detection: Detection section from Sigma rule for field values
        """
        # Parse timeframe
        timeframe_ms = self.parse_timeframe(timeframe_str)
        
        # Extract selections
        selections = self.extract_selections_from_condition(condition_node)
        
        if not selections:
            return "// No selections found for temporal monitor"
        
        # Generate RML
        rml_parts = []
        
        # Add selection definitions
        rml_parts.append("// Selection definitions")
        rml_parts.append(self.generate_selection_definitions(selections, detection or {}))
        rml_parts.append("")
        
        # Add temporal monitor
        rml_parts.append("// Temporal monitor")
        rml_parts.append(self.generate_temporal_monitor(selections, timeframe_ms))
        
        return "\n".join(rml_parts)

class EnhancedTemporalNode(ASTNode):
    """Enhanced temporal node that can handle complex conditions with timeframe"""
    
    def __init__(self, condition_node: ASTNode, timeframe: str = None, detection: dict = None):
        self.condition_node = condition_node
        # For near operations, use 10s default instead of 5m
        self.timeframe = timeframe or "10s"
        self.detection = detection or {}
        self.generator = TemporalMonitorGenerator()
    
    def to_rml(self) -> str:
        """Convert enhanced temporal node to RML format"""
        try:
            # Extract the actual timeframe value from the timeframe string
            # The timeframe might be in format "timeframe:5m" or just "5m"
            if self.timeframe and ':' in self.timeframe:
                actual_timeframe = self.timeframe.split(':', 1)[1]
            else:
                actual_timeframe = self.timeframe
            
            return self.generator.generate_complete_temporal_rml(self.condition_node, actual_timeframe, self.detection)
        except Exception as e:
            return f"// Error generating temporal monitor: {str(e)}"
    
    def get_selections(self) -> List[str]:
        """Get list of selection names from the condition"""
        selections = self.generator.extract_selections_from_condition(self.condition_node)
        return [sel[0] for sel in selections]
    
    def get_timeframe_ms(self) -> int:
        """Get timeframe in milliseconds"""
        # Extract the actual timeframe value
        if self.timeframe and ':' in self.timeframe:
            actual_timeframe = self.timeframe.split(':', 1)[1]
        else:
            actual_timeframe = self.timeframe
        
        return self.generator.parse_timeframe(actual_timeframe)
