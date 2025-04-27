from .base import ASTNode

# --------- Basic Match Nodes ----------

class LogsourceFilterNode(ASTNode):
    def __init__(self, fields: dict):
        self.fields = fields

    def to_rml(self) -> str:
        conditions = ', '.join(f"{k.lower()}: '{v}'" for k, v in self.fields.items())
        return f"logsource matches {{{conditions}}};"


class ExistsNode(ASTNode):
    def __init__(self, field: str):
        self.field = field

    def to_rml(self) -> str:
        return f"exists matches {{{self.field}: _}};"


class SimpleMatchNode(ASTNode):
    def __init__(self, name: str, fields: dict, positive: bool = True):
        self.name = name
        self.fields = fields
        self.positive = positive

    def to_rml(self) -> str:
        conditions = ', '.join(f"{k.lower()}: '{v}'" for k, v in self.fields.items())
        if self.positive:
            return f"{self.name} matches {{{conditions}}};"
        else:
            return f"{self.name} not matches {{{conditions}}};"


class ComparisonNode(ASTNode):
    def __init__(self, field: str, operator: str, value: str):
        self.field = field
        self.operator = operator
        self.value = value

    def to_rml(self) -> str:
        op_map = {
            "gt": ">", "gte": ">=", "lt": "<", "lte": "<=",
            "minute": "0 < x <", "hour": "0 < x <", "day": "0 < x <",
            "week": "0 < x <", "month": "0 < x <", "year": "0 < x <"
        }
        if self.operator in ["gt", "gte", "lt", "lte"]:
            return f"{self.field} {op_map[self.operator]} {self.value};"
        elif self.operator in ["minute", "hour", "day", "week", "month", "year"]:
            return f"{self.field} {op_map[self.operator]} {self.value};"
        else:
            return f"// Unsupported comparison modifier on {self.field}"


class ListOrNode(ASTNode):
    def __init__(self, base_field: str, values: list):
        self.base_field = base_field
        self.values = values

    def to_rml(self) -> str:
        rmls = []
        for idx, val in enumerate(self.values):
            rmls.append(f"no_{self.base_field}_{idx+1} not matches {{{self.base_field.lower()}: '{val}'}};")
        return '\n'.join(rmls)

# --------- Control/Unsupported Nodes ----------

class UnsupportedNode(ASTNode):
    def __init__(self, reason: str):
        self.reason = reason

    def to_rml(self) -> str:
        return f"// Translation not supported: {self.reason}"


# --------- Logical Composition Nodes ----------

class AndNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def to_rml(self) -> str:
        return f"({self.left.to_rml()} /\\ {self.right.to_rml()})"

class OrNode(ASTNode):
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right

    def to_rml(self) -> str:
        return f"({self.left.to_rml()} \\/ {self.right.to_rml()})"

class NotNode(ASTNode):
    def __init__(self, node: ASTNode):
        self.node = node

    def to_rml(self) -> str:
        # Apply negation at runtime (handled outside depending on match type)
        return f"(not {self.node.to_rml()})"

