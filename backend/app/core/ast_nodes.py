from .base import ASTNode

class SigmaCondition(ASTNode):
    def __init__(self, name: str, fields: dict):
        self.name = name
        self.fields = fields

    def to_rml(self) -> str:
        field_strs = []
        for k, v in self.fields.items():
            if k.endswith(":~"):
                field_strs.append(f"{k[:-2]}:~\"{v}\"")
            else:
                field_strs.append(f"{k}: \"{v}\"")
        return f"{self.name}() matches {{{', '.join(field_strs)}}};"

# backend/app/core/ast_nodes.py — unchanged SigmaRule
class SigmaRule(ASTNode):
    def __init__(self, conditions: list[ASTNode], main: str):
        self.conditions = conditions
        self.main = main

    def to_rml(self) -> str:
        parts = [cond.to_rml() for cond in self.conditions]
        parts.append(f"Main = {' & '.join([c.name for c in self.conditions if isinstance(c, SigmaCondition)])};")
        return '\n'.join(parts)
