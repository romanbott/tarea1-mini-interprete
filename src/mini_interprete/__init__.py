"""Mini interprete de expresiones aritmeticas.

    texto  ->  lexer  ->  tokens  ->  parser  ->  AST  ->  evaluator  ->  numero

La funcion `interpretar` es el punto de entrada para ejecutar todo el _pipeline_.
"""

from .evaluator import evaluar
from .lexer import tokenizar
from .parser import Parser


def interpretar(texto: str) -> int | float:
    """texto -> tokens -> AST -> valor."""
    return evaluar(Parser(tokenizar(texto)).parsear())
