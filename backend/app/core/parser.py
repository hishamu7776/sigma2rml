import yaml
import itertools
import re
from .ast.nodes import (
    LogsourceNode, ExistsNode, MatchNode,
    UnsupportedNode
)
from .ast.condition_parser import ConditionParser

class SigmaParser:
    def __init__(self):
        pass

    def parse(self, yaml_text: str):
        """
        Enhanced parser that handles complex Sigma patterns better
        """
        try:
            parsed = yaml.safe_load(yaml_text)
        except yaml.YAMLError as e:
            # Provide more helpful error message
            error_msg = str(e)
            if "mapping values are not allowed here" in error_msg:
                error_msg = "Invalid YAML syntax: Check for proper indentation and structure"
            elif "expected key" in error_msg:
                error_msg = "Invalid YAML syntax: Missing key or improper structure"
            raise ValueError(f"Invalid YAML format: {error_msg}")
        
        return self._parse_parsed_yaml(parsed)

    def parse_dict(self, parsed_dict: dict):
        """
        Parse a pre-parsed dictionary (useful for testing)
        """
        return self._parse_parsed_yaml(parsed_dict)

    def _parse_parsed_yaml(self, parsed):
        """
        Internal method to parse already-parsed YAML data
        """
        # Start with condition parsing to understand the logical structure
        detection = parsed.get('detection', {})
        condition_str = detection.get('condition', '')
        
        # Parse logsource
        logsource_node = self._parse_logsource(parsed.get('logsource', {}))
        
        # Parse detection selections
        match_nodes = self._parse_detections(detection)
        
        # Prepare available names for condition parsing
        available_names = list(match_nodes.keys())
        
        # Parse condition with the new robust parser
        cond_parser = ConditionParser(available_names)
        main_logic_ast = cond_parser.parse(condition_str)
        
        return {
            'logsource': logsource_node,
            'exists': [],  # We'll handle exists differently now
            'matches': [match_nodes[name] for name in match_nodes],
            'main': main_logic_ast,
            'unsupported': [],
            'original_condition': condition_str  # Store the original condition string
        }

    def _parse_logsource(self, logsource):
        """Parse logsource section"""
        if not logsource:
            return None
            
        # Handle more logsource fields
        product = logsource.get('product')
        service = logsource.get('service')
        category = logsource.get('category')
        
        if product or service or category:
            return LogsourceNode(product, service, category)
        return None

    def _parse_detections(self, detection):
        """Parse detection section with better handling of complex patterns"""
        match_nodes = {}
        
        for key, value in detection.items():
            if key.lower() == 'condition':
                continue
                
            if isinstance(value, dict):
                # This is a selection
                match_nodes[key] = MatchNode(key, value)
            elif isinstance(value, list):
                # Handle list values (like EventID: [4728, 4729, 4730])
                # This will be handled by the MatchNode.to_rml() method
                pass
            else:
                # Skip unsupported types
                continue
        
        return match_nodes
