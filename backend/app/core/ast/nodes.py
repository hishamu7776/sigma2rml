from .base import ASTNode

def format_value(val):
    if isinstance(val, (int, float)):
        return str(val)
    return f"'{val}'"


# ----------------------------------------
# Logical nodes (AND, OR, NOT)
# ----------------------------------------

class AndNode(ASTNode):
    def __init__(self, nodes):
        self.nodes = nodes

    def to_rml(self) -> str:
        return "(" + " /\\ ".join(node.to_rml() for node in self.nodes) + ")"

class OrNode(ASTNode):
    def __init__(self, nodes):
        self.nodes = nodes

    def to_rml(self) -> str:
        return "(" + " \\/ ".join(node.to_rml() for node in self.nodes) + ")"

# inside nodes.py

class NotNode(ASTNode):
    def __init__(self, node):
        self.node = node

    def to_rml(self) -> str:
        inner = self.node.to_rml()

        if isinstance(self.node, NameNode) and self.node.name.startswith("no_"):
            # remove 'no_' if it's no_selection type
            return self.node.name[3:]
        else:
            return "(~" + inner + ")"


# ----------------------------------------
# Reference node for match names
# ----------------------------------------

class NameNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def to_rml(self) -> str:
        return self.name

# ----------------------------------------
# Matches and Filters
# ----------------------------------------

class LogsourceFilterNode(ASTNode):
    def __init__(self, fields):
        self.fields = fields

    def to_rml(self) -> str:
        conditions = ', '.join(f"{k.lower()}: {self._format_value(v)}" for k, v in self.fields.items())
        return f"logsource matches {{{conditions}}};"

    def _format_value(self, val):
        if isinstance(val, (int, float)):
            return str(val)
        return f"'{val}'"

class ExistsNode(ASTNode):
    def __init__(self, field):
        self.field = field.lower()

    def to_rml(self) -> str:
        return f"exists matches {{{self.field}: _}};"

class SimpleMatchNode(ASTNode):
    def __init__(self, name, fields, positive=True):
        self.name = name
        self.fields = fields
        self.positive = positive

    def to_rml(self) -> str:
        fields = ', '.join(f"{k.lower()}: {self._format_value(v)}" for k, v in self.fields.items())
        if self.positive:
            return f"{self.name} matches {{{fields}}};"
        else:
            return f"{self.name} not matches {{{fields}}};"

    def _format_value(self, val):
        if isinstance(val, (int, float)):
            return str(val)
        return f"'{val}'"

class ComparisonMatchNode(ASTNode):
    def __init__(self, name):
        self.name = name
        self.fields = []  # list of (field, varname, operator, value)

    def add_condition(self, field, operator, value):
        var = 'x' if len(self.fields) == 0 else chr(ord('x') + len(self.fields))
        self.fields.append((field.lower(), var, operator, value))

    def to_rml(self) -> str:
        field_mapping = ', '.join(f"{field}: {var}" for field, var, _, _ in self.fields)
        conditions = ' && '.join(f"{var} {self._operator_symbol(op)} {self._format_value(val)}" for _, var, op, val in self.fields)
        return f"{self.name} not matches {{{field_mapping}}} with {conditions};"

    def _operator_symbol(self, op):
        return {
            'gt': '>',
            'gte': '>=',
            'lt': '<',
            'lte': '<='
        }.get(op, '??')

    def _format_value(self, val):
        if isinstance(val, (int, float)):
            return str(val)
        return f"'{val}'"

# ----------------------------------------
# Unsupported node for fallback
# ----------------------------------------

class UnsupportedNode(ASTNode):
    def __init__(self, reason):
        self.reason = reason

    def to_rml(self) -> str:
        return f"// Translation not supported: {self.reason}"
