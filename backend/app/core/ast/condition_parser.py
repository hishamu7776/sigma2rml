# backend/app/core/ast/condition_parser.py

import re
from .nodes import AndNode, OrNode, NotNode, UnsupportedNode

class ConditionParser:
    def __init__(self, available_selections: dict):
        """
        available_selections: mapping from Sigma term (selection, filter, etc.) to AST node name (no_selection, filter, etc.)
        """
        self.available = available_selections

    def parse(self, condition_str: str):
        """
        Parses a Sigma condition string into an AST Node.
        """
        self.tokens = self.tokenize(condition_str)
        self.pos = 0
        return self.expression()

    def tokenize(self, text: str):
        """
        Splits condition text into tokens (words, parens).
        """
        # Split on spaces and parentheses
        return re.findall(r'\w+\*?|\(|\)|and|or|not|of|1|all|any', text.lower())

    def expression(self):
        """
        Parses expression grammar.
        """
        node = self.term()
        
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token.lower() == 'and':
                self.pos += 1
                node = AndNode(node, self.term())
            elif token.lower() == 'or':
                self.pos += 1
                node = OrNode(node, self.term())
            else:
                break

        return node

    def term(self):
        """
        Parses a single term (possibly with not or parentheses).
        """
        token = self.tokens[self.pos]

        if token == '(':
            self.pos += 1
            node = self.expression()
            if self.tokens[self.pos] != ')':
                raise SyntaxError('Missing closing parenthesis')
            self.pos += 1
            return node

        elif token.lower() == 'not':
            self.pos += 1
            return NotNode(self.term())

        elif token.lower() in ['any', '1', 'all']:
            return self.multi_selection(token.lower())

        else:
            self.pos += 1
            return self.lookup(token)

    def multi_selection(self, token_type):
        """
        Parses 'any of selection*' or 'all of filter*'
        """
        if self.tokens[self.pos] not in ['of']:
            raise SyntaxError('Expected "of" after "any" or "all"')
        self.pos += 1
        selection_prefix = self.tokens[self.pos]
        self.pos += 1

        matching = [k for k in self.available.keys() if k.startswith(selection_prefix.rstrip('*'))]
        if not matching:
            return UnsupportedNode(f"No matching selections for pattern {selection_prefix}")

        nodes = [self.lookup(m) for m in matching]
        if token_type in ['any', '1']:
            return self.chain_or(nodes)
        elif token_type == 'all':
            return self.chain_and(nodes)
        else:
            return UnsupportedNode("Unknown multi-selection")

    def lookup(self, term):
        """
        Find the correct AST node name for a given condition reference.
        """
        term = term.rstrip(')')
        mapped = self.available.get(term)
        if not mapped:
            return UnsupportedNode(f"Selection {term} not available")
        # Just return the string here; during transpilation, the RML finalization will apply correct quoting.
        return mapped

    def chain_and(self, nodes):
        """
        Build an AndNode chain for multiple nodes.
        """
        if not nodes:
            return UnsupportedNode("Empty AND group")
        node = nodes[0]
        for n in nodes[1:]:
            node = AndNode(node, n)
        return node

    def chain_or(self, nodes):
        """
        Build an OrNode chain for multiple nodes.
        """
        if not nodes:
            return UnsupportedNode("Empty OR group")
        node = nodes[0]
        for n in nodes[1:]:
            node = OrNode(node, n)
        return node
