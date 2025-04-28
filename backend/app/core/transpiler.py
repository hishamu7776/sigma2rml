# backend/app/core/transpiler.py

from .ast.nodes import ASTNode
from .parser import SigmaParser

class SigmaToRMLTranspiler:
    def __init__(self):
        self.parser = SigmaParser()

    def transpile(self, yaml_text: str):
        ast = self.parser.parse(yaml_text)

        lines = []

        # 1. Logsource
        if ast['logsource']:
            lines.append(ast['logsource'].to_rml())

        # 2. Exists (exists chain)
        for exist_node in ast['exists']:
            lines.append(exist_node.to_rml())

        # 3. Match rules
        for match_node in ast['matches']:
            lines.append(match_node.to_rml())

        # 4. Unsupported items
        for unsupported_node in ast['unsupported']:
            lines.append(unsupported_node.to_rml())

        # 5. Main logic
        if ast['main']:
            main_expr = ast['main'].to_rml()
            if ast['logsource']:
                main_expr = f"Main = logsource >> ({main_expr} (Main \\/ empty));"
            else:
                main_expr = f"Main = ({main_expr} (Main \\/ empty));"
            lines.append(main_expr)
        else:
            lines.append("// Translation not supported: Main expression not available")

        return "\n".join(lines)
