import yaml
import itertools
from .ast.nodes import (
    LogsourceFilterNode, ExistsNode, SimpleMatchNode,
    ComparisonMatchNode, UnsupportedNode
)
from .ast.condition_parser import ConditionParser

class SigmaParser:
    def __init__(self):
        pass

    def parse(self, yaml_text: str):
        parsed = yaml.safe_load(yaml_text)

        logsource_node = None
        exists_nodes = []
        match_nodes = {}
        unsupported_nodes = []

        detection = parsed.get('detection', {})
        logsource = parsed.get('logsource', {})

        unsupported_modifiers = [
            'startswith', 'endswith', 'contains', 'cased', 'windash',
            're', 'fieldref', 'expand', 'base64', 'cidr'
        ]

        # 1. Parse logsource
        if logsource:
            log_fields = {k: v for k, v in logsource.items() if k.lower() in ['category', 'product', 'service']}
            if log_fields:
                logsource_node = LogsourceFilterNode(log_fields)

        # 2. Parse detection
        for key, value in detection.items():
            if key.lower() == 'condition':
                continue

            if isinstance(value, dict):
                fixed_fields = {}
                list_fields = {}
                special_handled = False
                comparison_node = None

                for k, v in value.items():
                    if '|' in k:
                        field, *mods = k.split('|')
                        field = field.strip()

                        if any(m in mods for m in ['gt', 'gte', 'lt', 'lte']):
                            operator = [m for m in mods if m in ['gt', 'gte', 'lt', 'lte']][0]

                            if not comparison_node:
                                comparison_node = ComparisonMatchNode(name=f"no_{key}")

                            comparison_node.add_condition(field, operator, v)
                            special_handled = True
                            continue

                        elif 'exists' in mods:
                            exists_nodes.append(ExistsNode(field))
                            fixed_fields[field] = v

                        elif any(m in mods for m in unsupported_modifiers):
                            unsupported_nodes.append(UnsupportedNode(f"Modifier(s) {mods} not supported yet under field '{field}'"))
                            continue

                        else:
                            unsupported_nodes.append(UnsupportedNode(f"Modifier(s) {mods} unknown or not handled yet under field '{field}'"))
                            continue

                    else:
                        if isinstance(v, list):
                            list_fields[k] = v
                        else:
                            fixed_fields[k] = v

                if special_handled:
                    match_nodes[key] = [comparison_node]
                elif list_fields:
                    list_keys = list(list_fields.keys())
                    list_values = [list_fields[k] for k in list_keys]

                    exploded_nodes = []
                    count = 1

                    for combination in itertools.product(*list_values):
                        fields_combined = dict(fixed_fields)
                        for idx, val in enumerate(combination):
                            fields_combined[list_keys[idx]] = val
                        exploded_nodes.append(SimpleMatchNode(f"no_{key}{count}", fields_combined, positive=False))
                        count += 1

                    match_nodes[key] = exploded_nodes
                else:
                    match_nodes[key] = [SimpleMatchNode(f"no_{key}", fixed_fields, positive=False)]

            elif isinstance(value, list):
                if all(isinstance(item, str) for item in value):
                    unsupported_nodes.append(UnsupportedNode(f"Keyword-style matching not supported under '{key}'"))
                else:
                    unsupported_nodes.append(UnsupportedNode(f"Unsupported structure under '{key}' (non-string list)"))

            else:
                unsupported_nodes.append(UnsupportedNode(f"Unsupported structure under '{key}'"))

        # 3. Prepare available names properly
        available_names = {}
        for k, nodes in match_nodes.items():
            if isinstance(nodes, list) and len(nodes) > 1:
                available_names[k] = [node.name for node in nodes]
            else:
                available_names[k] = nodes[0].name

        # 4. Parse condition
        condition_str = detection.get('condition', '')
        cond_parser = ConditionParser(available_names)
        main_logic_ast = cond_parser.parse(condition_str)

        # 5. Assemble final AST dict
        return {
            'logsource': logsource_node,
            'exists': exists_nodes,
            'matches': [node for nodes in match_nodes.values() for node in nodes],
            'main': main_logic_ast,
            'unsupported': unsupported_nodes
        }
