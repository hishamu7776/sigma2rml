
from abc import ABC, abstractmethod

class ASTNode(ABC):
    """
    Base class for all AST nodes.
    Every node must implement a `to_rml` method.
    """

    @abstractmethod
    def to_rml(self) -> str:
        """
        Convert the node to RML code.
        """
        pass
