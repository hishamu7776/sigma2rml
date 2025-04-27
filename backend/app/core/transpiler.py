# backend/app/core/transpiler.py

from .parser import SigmaParser
from .ast.nodes import UnsupportedNode

class SigmaToRMLTranspiler:
    def __init__(self):
        self.parser = SigmaParser()

    def transpile(self, yaml_text: str) -> str:
        ast = self.parser.parse(yaml_text)

        # 1. If any unsupported features, fail early
        if ast['unsupported']:
            reasons = '\n'.join(node.to_rml() for node in ast['unsupported'])
            return f"// Translation not supported due to:\n{reasons}"

        rml_lines = []

        # 2. Handle Logsource if exists
        if ast['logsource']:
            rml_lines.append(ast['logsource'].to_rml())

        # 3. Handle Exists filters
        for exists_node in ast['exists']:
            rml_lines.append(exists_node.to_rml())

        # 4. Handle Match nodes (selection/filter/other fields)
        for match_node in ast['matches']:
            rml_lines.append(match_node.to_rml())
        # 5. Handle Main condition logic
        main_logic_rml = self.build_main(ast)
        rml_lines.append(main_logic_rml)
        return '\n'.join(rml_lines)

    def build_main(self, ast: dict) -> str:
        """
        Build Main = ... RML expression with correct chaining.
        """
        chain = []

        if ast['logsource']:
            chain.append("logsource")

        if ast['exists']:
            for idx, _ in enumerate(ast['exists']):
                chain.append(f"exists")

        main_logic_expr = self.render_main_logic(ast['main'])

        # Assemble chaining
        while len(chain) > 0:
            node = chain.pop()
            main_logic_expr = f"{node} >> ({main_logic_expr})"

        return f"Main = {main_logic_expr};"

    def render_main_logic(self, main_ast) -> str:
        """
        Recursively render Main logical AST.
        """
        if isinstance(main_ast, str):
            # simple case: single selection name
            return f"{main_ast} (Main \\/ empty)"
        else:
            # Complex case: AND, OR, etc.
            inner = main_ast.to_rml()
            return f"{inner} (Main \\/ empty)"
