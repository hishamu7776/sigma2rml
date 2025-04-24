from .base import ASTNode

class RMLCodeEmitter:
    def emit(self, node: ASTNode) -> str:
        return node.to_rml()

