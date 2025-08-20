import re
from .nodes import AndNode, OrNode, NotNode, NameNode, UnsupportedNode, TemporalNode, QuantifierNode
from .temporal_monitor import EnhancedTemporalNode

class ConditionParser:
    def __init__(self, available_names, detection: dict = None):
        """
        available_names: list of selection names
        detection: detection section from Sigma rule for field values
        """
        self.available_names = available_names
        self.detection = detection or {}
        self.tokens = []
        self.pos = 0
        self.temporal_operators = ['near', 'before', 'after', 'within']
        self.timeframe_pattern = re.compile(r'(\d+[smhd])', re.IGNORECASE)

    def parse(self, condition_str):
        """Main parsing entry point - start with condition to understand structure"""
        if not condition_str:
            return UnsupportedNode("No condition specified")
        
        self.tokens = self.tokenize(condition_str)
        self.pos = 0
        
        # Check if this is a temporal condition with timeframe
        if self._has_timeframe(condition_str):
            return self._parse_temporal_condition()
        else:
            return self.expression()

    def _has_timeframe(self, condition_str: str) -> bool:
        """Check if condition contains a timeframe specification"""
        # Check for timeframe patterns in the condition string
        if self.timeframe_pattern.search(condition_str):
            return True
        
        # Also check if the condition string contains "timeframe" keyword
        if "timeframe" in condition_str.lower():
            return True
        
        # Check for near operator which indicates temporal behavior
        if "| near" in condition_str.lower():
            return True
        
        return False

    def _parse_temporal_condition(self):
        """Parse temporal condition with timeframe"""
        # First check if this is a near operator condition
        if self._has_near_operator():
            return self._parse_near_condition()
        
        # Parse the regular condition part
        condition_node = self.expression()
        
        # Look for timeframe in the tokens or condition string
        timeframe = self._extract_timeframe()
        
        # Create enhanced temporal node with detection information
        return EnhancedTemporalNode(condition_node, timeframe, self.detection)

    def _has_near_operator(self) -> bool:
        """Check if tokens contain a near operator pattern"""
        for i, token in enumerate(self.tokens):
            if token == '|' and i + 1 < len(self.tokens) and self.tokens[i + 1].lower() == 'near':
                return True
        return False

    def _parse_near_condition(self):
        """Parse near operator condition and convert to AND operation"""
        # Find the near operator position
        near_pos = -1
        for i, token in enumerate(self.tokens):
            if token == '|' and i + 1 < len(self.tokens) and self.tokens[i + 1].lower() == 'near':
                near_pos = i
                break
        
        if near_pos == -1:
            # Fallback to regular parsing
            return self.expression()
        
        # Extract the two selections around the near operator
        if near_pos > 0 and near_pos + 2 < len(self.tokens):
            selection1 = self.tokens[near_pos - 1]
            selection2 = self.tokens[near_pos + 2]  # Skip | and near
            
            # Create an AND node with the two selections
            left_node = NameNode(selection1)
            right_node = NameNode(selection2)
            and_node = AndNode(left_node, right_node)
            
            # Extract timeframe
            timeframe = self._extract_timeframe()
            
            # Create enhanced temporal node
            return EnhancedTemporalNode(and_node, timeframe, self.detection)
        
        # Fallback to regular parsing
        return self.expression()

    def _extract_timeframe(self) -> str:
        """Extract timeframe from tokens or detection section"""
        # First check tokens for timeframe patterns
        for token in self.tokens:
            if self.timeframe_pattern.match(token):
                return token
        
        # If no timeframe found in tokens, check if we have a timeframe field in detection
        if self.detection and 'timeframe' in self.detection:
            return self.detection['timeframe']
        
        # Default timeframe if none found
        return "5m"

    def tokenize(self, text):
        """
        Enhanced tokenization that handles complex Sigma patterns
        """
        # More comprehensive pattern matching
        patterns = [
            r'all of them',
            r'any of them', 
            r'all of',
            r'any of',
            r'1 of',
            r'2 of',
            r'3 of',
            r'4 of',
            r'5 of',
            r'6 of',
            r'7 of',
            r'8 of',
            r'9 of',
            r'\d+ of',
            r'\w+\*',  # selection* 
            r'\(', r'\)',
            r'and', r'or', r'not',
            r'\|',  # temporal operator separator
            r'near', r'before', r'after', r'within', r'count',
            r'>\d+',  # comparison operators with numbers (must come before [<>]=?)
            r'[<>]=?',  # comparison operators
            r'\d+[smhd]',  # timeframe patterns (5m, 10s, 2h, 1d)
            r'\w+',  # identifiers
            r'[^\s]+'  # catch any remaining tokens
        ]
        
        # Join patterns and find all matches
        pattern = '|'.join(patterns)
        tokens = re.findall(pattern, text, flags=re.IGNORECASE)
        
        # Clean up tokens and handle special cases
        cleaned_tokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i].strip()
            if not token:
                i += 1
                continue
            
            # Handle numbered quantifiers
            if re.match(r'\d+ of', token, re.IGNORECASE):
                cleaned_tokens.append(token)
                i += 1
                continue
                
            cleaned_tokens.append(token)
            i += 1
            
        return cleaned_tokens

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek_token(self, offset=1):
        """Look ahead at tokens without consuming them"""
        peek_pos = self.pos + offset
        return self.tokens[peek_pos] if peek_pos < len(self.tokens) else None

    def eat(self, token=None):
        current = self.current_token()
        if token is None or (current and current.lower() == token.lower()):
            self.pos += 1
            return current
        else:
            raise ValueError(f"Expected token {token}, but got {current}")

    def expression(self):
        """
        Parse expression with OR precedence: expr OR expr OR expr
        """
        node = self.term()

        while self.current_token() and self.current_token().lower() == 'or':
            self.eat('or')
            right = self.term()
            node = OrNode(node, right)

        return node

    def term(self):
        """
        Parse term with AND precedence: term AND term AND term
        """
        node = self.factor()

        while self.current_token() and self.current_token().lower() == 'and':
            self.eat('and')
            right = self.factor()
            node = AndNode(node, right)

        return node

    def factor(self):
        """
        Parse factor: NOT factor | (expression) | identifier | quantifier
        """
        token = self.current_token()
        
        if not token:
            raise ValueError("Unexpected end of input")
        
        if token.lower() == 'not':
            self.eat('not')
            operand = self.factor()
            return NotNode(operand)
        
        elif token == '(':
            self.eat('(')
            expr = self.expression()
            if self.current_token() == ')':
                self.eat(')')
                return expr
            else:
                raise ValueError("Expected closing parenthesis")
        
        elif token.lower() in ['all of them', 'any of them']:
            self.eat()
            return QuantifierNode(token.lower(), self.available_names)
        
        elif re.match(r'\d+ of', token, re.IGNORECASE):
            self.eat()
            # Look for selection* pattern
            if self.current_token() and self.current_token().endswith('*'):
                selection = self.eat()
                # Extract the base name without the *
                base_name = selection[:-1]
                # Find all available names that start with this base name
                matching_names = [name for name in self.available_names if name.startswith(base_name)]
                if matching_names:
                    return QuantifierNode(token.lower(), matching_names)
                else:
                    return QuantifierNode(token.lower(), [base_name])
            else:
                return QuantifierNode(token.lower(), [])
        
        elif token.endswith('*'):
            # Handle selection* pattern
            self.eat()
            base_name = token[:-1]  # Remove the *
            # Find all available names that start with this base name
            matching_names = [name for name in self.available_names if name.startswith(base_name)]
            if matching_names:
                return QuantifierNode("all of", matching_names)
            else:
                return QuantifierNode("all of", [base_name])
        
        elif token in self.available_names:
            self.eat()
            # Check if this is followed by a temporal operator
            if self.current_token() == '|':
                self.eat('|')  # Consume the |
                temporal_op = self.current_token()
                if temporal_op in ['near', 'before', 'after', 'within', 'count']:
                    self.eat()  # Consume the temporal operator
                    
                    if temporal_op == 'count':
                        # Handle count() case
                        if self.current_token() == '(':
                            self.eat('(')  # Consume (
                            if self.current_token() == ')':
                                self.eat(')')  # Consume )
                                # Look for comparison
                                if self.current_token() and '>' in self.current_token():
                                    count_expr = self.eat()
                                    # Also consume the number after >
                                    if self.current_token() and self.current_token().isdigit():
                                        count_expr += self.eat()
                                    # Clean up the count expression (remove duplicate >)
                                    if count_expr.startswith('>') and count_expr.count('>') > 1:
                                        count_expr = count_expr.replace('>>', '>')
                                    # Extract just the number for the comparison
                                    if '>' in count_expr:
                                        try:
                                            count_num = int(count_expr.split('>')[1])
                                            return TemporalNode(token, 'count', None, None, count_num)
                                        except (ValueError, IndexError):
                                            return TemporalNode(token, 'count', None, None, count_expr)
                                    else:
                                        return TemporalNode(token, 'count', None, None, count_expr)
                                else:
                                    return TemporalNode(token, 'count', None, None, "5")
                            else:
                                return TemporalNode(token, 'count', None, None, "5")
                        else:
                            return TemporalNode(token, 'count', None, None, "5")
                    else:
                        # Handle other temporal operators
                        selection2 = None
                        if self.current_token() and self.current_token() in self.available_names:
                            selection2 = self.eat()
                        return TemporalNode(token, temporal_op, selection2)
                else:
                    # Unknown temporal operator, treat as regular identifier
                    pass
            
            return NameNode(token)
        
        else:
            # Unknown token, treat as identifier
            self.eat()
            return NameNode(token)

    def safe_wrap(self, node):
        """Safely wrap a node if needed"""
        return node
