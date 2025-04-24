import yaml
from .ast_nodes import SigmaCondition, SigmaRule

class SigmaParser:
    def parse(self, yaml_text: str) -> SigmaRule:
        data = yaml.safe_load(yaml_text)
        detection = data.get("detection", {})
        conditions = []
        for key, val in detection.items():
            if key != "condition":
                conditions.append(SigmaCondition(key, val))
        return SigmaRule(conditions, detection.get("condition", ""))
