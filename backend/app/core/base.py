from abc import ABC, abstractmethod

class ASTNode(ABC):
    @abstractmethod
    def to_rml(self) -> str:
        pass

class Transpiler(ABC):
    @abstractmethod
    def parse(self, input_str: str) -> ASTNode:
        pass

    @abstractmethod
    def emit(self, node: ASTNode) -> str:
        pass