from .base import Transpiler
from .parser import SigmaParser
from .emitter import RMLCodeEmitter

class SigmaToRMLTranspiler(Transpiler):
    def __init__(self):
        self.parser = SigmaParser()
        self.emitter = RMLCodeEmitter()

    def parse(self, input_str: str):
        return self.parser.parse(input_str)

    def emit(self, node):
        return self.emitter.emit(node)

    def transpile(self, input_str: str) -> str:
        ast = self.parse(input_str)
        return self.emit(ast)
