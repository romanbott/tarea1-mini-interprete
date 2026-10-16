"""Los comandos de la linea de comandos.

Cada comando recibe el texto de una expresion y regresa el texto que hay que
imprimir.
"""

from collections.abc import Callable

from . import interpretar
from .ast import formatear_arbol
from .lexer import tokenizar
from .parser import Parser


def _evaluar(texto: str) -> str:
    """El valor de la expresion."""
    return str(interpretar(texto))


def _arbol(texto: str) -> str:
    """El AST dibujado como arbol."""
    return "\n".join(formatear_arbol(Parser(tokenizar(texto)).parsear()))


COMANDOS: dict[str, Callable[[str], str]] = {
    "evaluar": _evaluar,
    "arbol": _arbol,
}
