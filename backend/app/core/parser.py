# backend/app/core/parser.py

import yaml
from .ast.nodes import (
    LogsourceFilterNode, ExistsNode, SimpleMatchNode,
    ListOrNode, ComparisonNode, UnsupportedNode
)
from .ast.condition_parser import ConditionParser

class SigmaParser:
    def __init__(self):
        pass

    def parse(self, yaml_text: str):
        """
        Parses Sigma YAML into AST tree.
        """
        parsed = yaml.safe_load(yaml_text)

        logsource_node = None
        exists_nodes = []
        match_nodes = {}
        unsupported_nodes = []

        detection = parsed.get('detection', {})
        logsource = parsed.get('logsource', {})

        # 1. Parse logsource if available
        if logsource:
            log_fields = {k: v for k, v in logsource.items() if k.lower() in ['category', 'product', 'service']}
            if log_fields:
                logsource_node = LogsourceFilterNode(log_fields)

        # 2. Parse detection fields
        for key, value in detection.items():
            if key.lower() == 'condition':
                continue  # Handle condition separately
            if isinstance(value, dict):
                fields = {}
                for k, v in value.items():
                    if '|' in k:
                        field, *mods = k.split('|')
                        field = field.strip()

                        if 'exists' in mods:
                            exists_nodes.append(ExistsNode(field))
                        elif any(m in mods for m in ['gt', 'lt', 'gte', 'lte', 'minute', 'hour', 'day', 'week', 'month', 'year']):
                            # Only basic comparisons supported
                            operator = mods[-1]
                            exists_nodes.append(ComparisonNode(field, operator, v))
                        else:                            
                            unsupported_nodes.append(UnsupportedNode(f"Modifier(s) {mods} not supported yet"))
                    else:
                        fields[k] = v

                if fields:
                    # Normal match node
                    name = f"no_{key}"  # default to negated form
                    match_nodes[key] = SimpleMatchNode(name, fields, positive=False)

            elif isinstance(value, list):
                # list means or operation
                match_nodes[key] = ListOrNode(key, value)

            else:
                unsupported_nodes.append(UnsupportedNode(f"Unsupported structure under {key}"))

        # 3. Build condition logic
        condition_str = detection.get('condition', '')
        print(condition_str)
        available_names = {}
        for key, match_node in match_nodes.items():
            available_names[key] = match_node.name   # 'selection' => 'no_selection'
            # Also map the match node's own output name (no_selection) to itself
            available_names[match_node.name] = match_node.name            

        cond_parser = ConditionParser(available_names)
        main_logic_ast = cond_parser.parse(condition_str)
        # 4. Package everything into final assembly
        return {
            'logsource': logsource_node,
            'exists': exists_nodes,
            'matches': list(match_nodes.values()),
            'main': main_logic_ast,
            'unsupported': unsupported_nodes
        }
