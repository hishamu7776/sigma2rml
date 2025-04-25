import yaml
from .ast_nodes import SigmaCondition, SigmaRule

class SigmaParser:
    def parse(self, yaml_text: str) -> SigmaRule:
        data = yaml.safe_load(yaml_text)

        detection = data.get("detection", {})
        logsource = data.get("logsource", {})

        conditions = []

        # Translate logsource to a condition
        log_fields = {k: v for k, v in logsource.items() if k in ["category", "product", "service"]}
        if log_fields:
            conditions.append(SigmaCondition("logsourceFilter", log_fields))

        # Translate detection selections
        for key, val in detection.items():
            if key != "condition":
                transformed = {}
                for k, v in val.items():
                    # Translate wildcard/regex suffix (e.g. endswith)
                    if "|endswith" in k:
                        base_key = k.split("|", 1)[0]
                        escaped = v.replace('.', '\\\\.')
                        transformed[base_key + ":~"] = f"{escaped}$"

                    else:
                        transformed[k] = v
                conditions.append(SigmaCondition(key, transformed))

        return SigmaRule(conditions, detection.get("condition", ""))