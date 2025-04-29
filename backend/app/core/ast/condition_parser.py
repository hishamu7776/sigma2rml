import re
from .nodes import AndNode, OrNode, NotNode, NameNode, UnsupportedNode

class ConditionParser:
    def __init__(self, available_names):
        """
        available_names: mapping like selection1 -> [no_selection11, no_selection12]
        """
        self.available_names = available_names
        self.tokens = []
        self.pos = 0

    def parse(self, condition_str):
        self.tokens = self.tokenize(condition_str)
        self.pos = 0
        return self.expression()

    def tokenize(self, text):
        """
        Splits condition text into tokens (words, parentheses, etc.)
        """
        return re.findall(r'all of them|any of them|all of|any of|1 of|\w+\*?|\(|\)|and|or|not', text, flags=re.IGNORECASE)

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token=None):
        current = self.current_token()
        if token is None or (current and current.lower() == token.lower()):
            self.pos += 1
            return current
        else:
            raise ValueError(f"Expected token {token}, but got {current}")

    def expression(self):
        """
        Parse expression with OR precedence
        """
        node = self.term()

        while self.current_token() and self.current_token().lower() == 'or':
            self.eat('or')
            right = self.term()
            node = OrNode([self.safe_wrap(node), self.safe_wrap(right)])

        return node

    def term(self):
        """
        Parse term with AND precedence
        """
        node = self.factor()

        while self.current_token() and self.current_token().lower() == 'and':
            self.eat('and')
            right = self.factor()
            node = AndNode([self.safe_wrap(node), self.safe_wrap(right)])

        return node

    def factor(self):
        """
        Parse factor: not / parentheses / base item
        """
        token = self.current_token()

        if not token:
            raise ValueError("Unexpected end of tokens")

        token_lower = token.lower()

        if token_lower == 'not':
            self.eat('not')
            node = self.factor()
            return NotNode(self.safe_wrap(node))

        elif token == '(':
            self.eat('(')
            node = self.expression()
            self.eat(')')
            return node

        elif token_lower in ('any of', '1 of'):
            return self.any_all_of_node(any_of=True)

        elif token_lower == 'all of':
            return self.any_all_of_node(any_of=False)

        elif token_lower == 'any of them':
            return self.all_any_of_them_node(any_of=True)

        elif token_lower == 'all of them':
            return self.all_any_of_them_node(any_of=False)

        else:
            name = self.eat()
            return self.resolve_name(name)

    def resolve_name(self, name):
        """
        Resolve a selection name into appropriate AST node:
        - If multiple matches: wrap into OR
        - If one match: NameNode directly
        - If not found: UnsupportedNode
        """
        if name in self.available_names:
            value = self.available_names[name]

            if isinstance(value, list):
                if len(value) == 1:
                    return NameNode(value[0])
                else:
                    return OrNode([NameNode(v) for v in value])

            elif isinstance(value, str):
                return NameNode(value)

            else:
                return UnsupportedNode(f"Unsupported mapping for name {name}")

        else:
            return UnsupportedNode(f"Unknown name: {name}")

    def any_all_of_node(self, any_of=True):
        """
        Handle 'any of selection*', '1 of selection*', and 'all of selection*'
        """
        if any_of:
            self.eat('any of') if self.current_token().lower() == 'any of' else self.eat('1 of')
        else:
            self.eat('all of')

        pattern = self.eat()

        matching = []
        for name, mapped in self.available_names.items():
            if pattern.endswith('*') and name.startswith(pattern[:-1]):
                if isinstance(mapped, list):
                    matching.extend(NameNode(m) for m in mapped)
                else:
                    matching.append(NameNode(mapped))

        if not matching:
            return UnsupportedNode(f"No matching names for pattern {pattern}")

        if any_of:
            return OrNode(matching)
        else:
            return AndNode(matching)

    def all_any_of_them_node(self, any_of=True):
        """
        Handle 'any of them' and 'all of them'
        """
        if any_of:
            self.eat('any of them')
        else:
            self.eat('all of them')

        matching = []
        for name, mapped in self.available_names.items():
            if isinstance(mapped, list):
                matching.extend(NameNode(m) for m in mapped)
            else:
                matching.append(NameNode(mapped))

        if not matching:
            return UnsupportedNode(f"No names found for 'them' pattern")

        if any_of:
            return OrNode(matching)
        else:
            return AndNode(matching)

    def safe_wrap(self, node):
        """
        Safe wrap nodes, keeping UnsupportedNode if necessary
        """
        if isinstance(node, UnsupportedNode):
            return node
        return node
