from .base import ASTNode

class SigmaCondition(ASTNode):
    def __init__(self, name: str, fields: dict):
        self.name = name
        self.fields = fields

    def to_rml(self) -> str:
        field_str = ', '.join([f"{k}:{repr(v)}" for k, v in self.fields.items()])
        return f"{self.name}() matches {{{field_str}}};"

class SigmaRule(ASTNode):
    def __init__(self, conditions: list[ASTNode], main: str):
        self.conditions = conditions
        self.main = main

    def to_rml(self) -> str:
        parts = [cond.to_rml() for cond in self.conditions]
        parts.append(f"Main = {self.main};")
        return '\n'.join(parts)