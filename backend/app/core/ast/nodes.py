# backend/app/core/ast/nodes.py

import re

class ASTNode:
    """Base class for all AST nodes"""
    
    def to_rml(self) -> str:
        """Convert node to RML representation"""
        raise NotImplementedError("Subclasses must implement to_rml")

class LogsourceNode(ASTNode):
    """Represents the logsource section"""
    
    def __init__(self, product: str = None, service: str = None, category: str = None):
        self.product = product
        self.service = service
        self.category = category
    
    def to_rml(self) -> str:
        """Convert logsource to RML format: logsource matches {product: 'windows', service: 'security'};"""
        parts = []
        if self.product:
            parts.append(f"product: '{self.product}'")
        if self.service:
            parts.append(f"service: '{self.service}'")
        if self.category:
            parts.append(f"category: '{self.category}'")
        
        if parts:
            return f"logsource matches {{{', '.join(parts)}}};"
        else:
            return "// No logsource specified"

class SelectionNode(ASTNode):
    """Represents a selection (detection rule)"""
    
    def __init__(self, name: str, fields: dict):
        self.name = name
        self.fields = fields
    
    def to_rml(self) -> str:
        """Convert selection to RML format: selection matches {eventid: 4663, accesses: 'DELETE'};"""
        field_pairs = []
        for field, value in self.fields.items():
            if isinstance(value, list):
                # Handle list values with OR operator
                if all(isinstance(v, str) for v in value):
                    quoted_values = [f"'{v}'" for v in value]
                    field_pairs.append(f"{field.lower()}: {' | '.join(quoted_values)}")
                else:
                    field_pairs.append(f"{field.lower()}: {' | '.join(str(v) for v in value)}")
            elif isinstance(value, str):
                field_pairs.append(f"{field.lower()}: '{value}'")
            else:
                field_pairs.append(f"{field.lower()}: '{value}'")
        
        return f"{self.name} matches {{{', '.join(field_pairs)}}};"
    
    def to_rml_content(self) -> str:
        """Return just the content part without the selection name"""
        field_pairs = []
        for field, value in self.fields.items():
            if isinstance(value, list):
                # Handle list values with OR operator
                if all(isinstance(v, str) for v in value):
                    quoted_values = [f"'{v}'" for v in value]
                    field_pairs.append(f"{field.lower()}: {' | '.join(quoted_values)}")
                else:
                    field_pairs.append(f"{field.lower()}: {' | '.join(str(v) for v in value)}")
            elif isinstance(value, str):
                field_pairs.append(f"{field.lower()}: '{value}'")
            else:
                field_pairs.append(f"{field.lower()}: {value}")
        
        return f"{{{', '.join(field_pairs)}}}"

class ExistsNode(ASTNode):
    """Represents an exists statement"""
    
    def __init__(self, field: str):
        self.field = field
    
    def to_rml(self) -> str:
        """Convert exists to RML format"""
        return f"// exists: {self.field}"

class MatchNode(ASTNode):
    """Represents a match statement"""
    
    def __init__(self, name: str, fields: dict):
        self.name = name
        self.fields = fields
    
    def to_rml(self) -> str:
        """Convert match to RML format: selection matches {eventid: 4663, accesses: 'DELETE'};"""
        field_pairs = []
        modifier_constraints = []
        modifier_counter = 1
        
        for field, value in self.fields.items():
            if isinstance(value, list):
                # Handle list values with OR operator
                if all(isinstance(v, str) for v in value):
                    quoted_values = [f"'{v}'" for v in value]
                    field_pairs.append(f"{field.lower()}: {' | '.join(quoted_values)}")
                else:
                    field_pairs.append(f"{field.lower()}: {' | '.join(str(v) for v in value)}")
            elif isinstance(value, str):
                field_pairs.append(f"{field.lower()}: '{value}'")
            else:
                # Check for comparison operators (only support lt, lte, gt, gte)
                if '|' in str(field):
                    base_field, operator = field.split('|', 1)
                    if operator in ['lt', 'lte', 'gt', 'gte']:
                        # Generate RML with comparison: {field: x1} with x1 <= value
                        field_pairs.append(f"{base_field.lower()}: x{modifier_counter}")
                        
                        # Convert operator to RML syntax
                        if operator == 'lt':
                            rml_op = '<'
                        elif operator == 'lte':
                            rml_op = '<='
                        elif operator == 'gt':
                            rml_op = '>'
                        elif operator == 'gte':
                            rml_op = '>='
                        else:
                            rml_op = '='
                        
                        modifier_constraints.append(f"x{modifier_counter} {rml_op} {value}")
                        modifier_counter += 1
                    else:
                        # Unsupported modifier - mark as unsupported
                        field_pairs.append(f"// UNSUPPORTED MODIFIER: {field.lower()}: {value} ({operator} not supported)")
                else:
                    field_pairs.append(f"{field.lower()}: {value}")
        
        # Build the RML string
        rml_content = f"{self.name} matches {{{', '.join(field_pairs)}}}"
        
        # Add modifier constraints if any
        if modifier_constraints:
            rml_content += f" with {' && '.join(modifier_constraints)}"
        
        return rml_content + ";"
    
    def to_rml_content(self) -> str:
        """Return just the content part without the selection name"""
        field_pairs = []
        modifier_constraints = []
        modifier_counter = 1
        
        for field, value in self.fields.items():
            if isinstance(value, list):
                # Handle list values with OR operator
                if all(isinstance(v, str) for v in value):
                    quoted_values = [f"'{v}'" for v in value]
                    field_pairs.append(f"{field.lower()}: {' | '.join(quoted_values)}")
                else:
                    field_pairs.append(f"{field.lower()}: {' | '.join(str(v) for v in value)}")
            elif isinstance(value, str):
                field_pairs.append(f"{field.lower()}: '{value}'")
            else:
                # Check for comparison operators (only support lt, lte, gt, gte)
                if '|' in str(field):
                    base_field, operator = field.split('|', 1)
                    if operator in ['lt', 'lte', 'gt', 'gte']:
                        # Generate RML with comparison: {field: x1} with x1 <= value
                        field_pairs.append(f"{base_field.lower()}: x{modifier_counter}")
                        
                        # Convert operator to RML syntax
                        if operator == 'lt':
                            rml_op = '<'
                        elif operator == 'lte':
                            rml_op = '<='
                        elif operator == 'gt':
                            rml_op = '>'
                        elif operator == 'gte':
                            rml_op = '>='
                        else:
                            rml_op = '='
                        
                        modifier_constraints.append(f"x{modifier_counter} {rml_op} {value}")
                        modifier_counter += 1
                    else:
                        # Unsupported modifier - mark as unsupported
                        field_pairs.append(f"// UNSUPPORTED MODIFIER: {field.lower()}: {value} ({operator} not supported)")
                else:
                    field_pairs.append(f"{field.lower()}: {value}")
        
        # Build the content string
        content = f"{{{', '.join(field_pairs)}}}"
        
        # Add modifier constraints if any
        if modifier_constraints:
            content += f" with {' && '.join(modifier_constraints)}"
        
        return content
    
    def get_comparison_constraints(self) -> list:
        """Get comparison constraints for fields with supported operators (lt, lte, gt, gte)"""
        constraints = []
        modifier_counter = 1
        
        for field, value in self.fields.items():
            if '|' in str(field):
                base_field, operator = field.split('|', 1)
                if operator in ['lt', 'lte', 'gt', 'gte']:
                    # Convert operator to RML syntax
                    if operator == 'lt':
                        rml_op = '<'
                    elif operator == 'lte':
                        rml_op = '<='
                    elif operator == 'gt':
                        rml_op = '>'
                    elif operator == 'gte':
                        rml_op = '>='
                    else:
                        rml_op = '='
                    
                    constraints.append(f"{base_field.lower()}: x{modifier_counter} with x{modifier_counter} {rml_op} {value}")
                    modifier_counter += 1
                # Note: Unsupported modifiers are handled in to_rml() method
        
        return constraints
    
    def get_negation_rml(self) -> str:
        """Generate negation using 'not matches' with opposite conditions"""
        field_pairs = []
        modifier_constraints = []
        modifier_counter = 1
        
        for field, value in self.fields.items():
            if isinstance(value, list):
                # Handle list values with OR operator
                if all(isinstance(v, str) for v in value):
                    quoted_values = [f"'{v}'" for v in value]
                    field_pairs.append(f"{field.lower()}: {' | '.join(quoted_values)}")
                else:
                    field_pairs.append(f"{field.lower()}: {' | '.join(str(v) for v in value)}")
            elif isinstance(value, str):
                field_pairs.append(f"{field.lower()}: '{value}'")
            else:
                # Check for comparison operators (only support lt, lte, gt, gte)
                if '|' in str(field):
                    base_field, operator = field.split('|', 1)
                    if operator in ['lt', 'lte', 'gt', 'gte']:
                        # Generate RML with comparison: {field: x1} with x1 [operator] value
                        field_pairs.append(f"{base_field.lower()}: x{modifier_counter}")
                        
                        # Convert operator to RML syntax (keep same operator for not matches)
                        if operator == 'lt':
                            rml_op = '<'
                        elif operator == 'lte':
                            rml_op = '<='
                        elif operator == 'gt':
                            rml_op = '>'
                        elif operator == 'gte':
                            rml_op = '>='
                        else:
                            rml_op = '='
                        
                        modifier_constraints.append(f"x{modifier_counter} {rml_op} {value}")
                        modifier_counter += 1
                    else:
                        # Unsupported modifier - mark as unsupported
                        field_pairs.append(f"// UNSUPPORTED MODIFIER: {field.lower()}: {value} ({operator} not supported)")
                else:
                    field_pairs.append(f"{field.lower()}: {value}")
        
        # Build the negation RML string
        safe_name = f"safe_{self.name}" if hasattr(self, 'name') else "safe_selection"
        rml_content = f"{safe_name} not matches {{{', '.join(field_pairs)}}}"
        
        # Add modifier constraints if any
        if modifier_constraints:
            rml_content += f" with {' && '.join(modifier_constraints)}"
        
        return rml_content + ";"

class AndNode(ASTNode):
    """Represents logical AND operation"""
    
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def to_rml(self) -> str:
        """Convert AND to RML format"""
        left_str = self.left.to_rml()
        right_str = self.right.to_rml()
        return f"({left_str} /\\ {right_str})"

class OrNode(ASTNode):
    """Represents logical OR operation"""
    
    def __init__(self, left: ASTNode, right: ASTNode):
        self.left = left
        self.right = right
    
    def to_rml(self) -> str:
        """Convert OR to RML format"""
        left_str = self.left.to_rml()
        right_str = self.right.to_rml()
        return f"({left_str} \\/ {right_str})"

class NotNode(ASTNode):
    """Represents logical NOT operation"""
    
    def __init__(self, operand: ASTNode):
        self.operand = operand
    
    def to_rml(self) -> str:
        """Convert NOT to RML format"""
        inner = self.operand.to_rml()
        if isinstance(self.operand, (NameNode, MatchNode)):
            # For simple nodes, use proper negation
            return "(~" + inner + ")"
        else:
            # For other nodes, use proper negation
            return "(~" + inner + ")"

class NameNode(ASTNode):
    """Represents a simple identifier"""
    
    def __init__(self, name: str):
        self.name = name
    
    def to_rml(self) -> str:
        """Convert name to RML format"""
        return self.name

class QuantifierNode(ASTNode):
    """Represents quantifiers like 'all of them', '1 of selection*'"""
    
    def __init__(self, quantifier: str, selections: list):
        self.quantifier = quantifier
        self.selections = selections
    
    def to_rml(self) -> str:
        """Convert quantifier to RML format"""
        if self.quantifier == "all of them":
            # all of them becomes (safe_selection1 \/ safe_selection2)*
            safe_selections = [f"safe_{sel}" for sel in self.selections]
            return f"({' \\/ '.join(safe_selections)})*"
        elif self.quantifier == "1 of":
            # 1 of becomes (safe_selection1 /\ safe_selection2)*
            safe_selections = [f"safe_{sel}" for sel in self.selections]
            return f"({' /\\ '.join(safe_selections)})*"
        elif re.match(r'\d+ of', self.quantifier):
            # Extract the number
            match = re.match(r'(\d+) of', self.quantifier)
            if match:
                n = int(match.group(1))
                if n == 1:
                    # 1 of becomes (safe_selection1 /\ safe_selection2)*
                    safe_selections = [f"safe_{sel}" for sel in self.selections]
                    return f"({' /\\ '.join(safe_selections)})*"
                else:
                    # For other numbers, use OR pattern
                    safe_selections = [f"safe_{sel}" for sel in self.selections]
                    return f"({' \\/ '.join(safe_selections)})*"
        else:
            # Default fallback
            return f"// Quantifier: {self.quantifier} of {self.selections}"

class TemporalNode(ASTNode):
    """Represents temporal operators like '| near', '| count'"""
    
    def __init__(self, selection1: str, operator: str, selection2: str = None, timeframe: str = None, count: int = None):
        self.selection1 = selection1
        self.operator = operator
        self.selection2 = selection2
        self.timeframe = timeframe or "10s"  # Default 10 seconds
        self.count = count
    
    def to_rml(self) -> str:
        """Convert temporal to RML format"""
        if self.operator == "near":
            return f"temporal_near({self.selection1}, {self.selection2}, {self.timeframe})"
        elif self.operator == "before":
            return f"temporal_before({self.selection1}, {self.selection2}, {self.timeframe})"
        elif self.operator == "after":
            return f"temporal_after({self.selection1}, {self.selection2}, {self.timeframe})"
        elif self.operator == "within":
            return f"temporal_within({self.selection1}, {self.selection2}, {self.timeframe})"
        elif self.operator == "count":
            return f"temporal_count({self.selection1}, {self.count}, {self.timeframe})"
        else:
            return f"// Unknown temporal operator: {self.operator}"

class UnsupportedNode(ASTNode):
    """Represents unsupported features"""
    
    def __init__(self, feature: str, description: str = ""):
        self.feature = feature
        self.description = description
    
    def to_rml(self) -> str:
        """Convert unsupported to RML format"""
        return f"// Unsupported feature: {self.feature} {self.description}"
