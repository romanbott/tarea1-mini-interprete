"""Del AST a un numero.

Recorre el arbol de abajo hacia arriba: para evaluar una operacion hay que
evaluar primero sus dos lados. El "que calcula" cada operador vive en el
catalogo `Operador`; aqui solo se le pide su funcion y se traducen los errores
de Python a los del interprete.
"""

from .ast import Nodo, Numero, OperacionBinaria
from .errores import ErrorDeEvaluacion


def evaluar(nodo: Nodo) -> int | float:
    """Evalua un nodo del AST y regresa su valor."""
    if isinstance(nodo, Numero):
        return nodo.valor

    if isinstance(nodo, OperacionBinaria):
        izquierda = evaluar(nodo.izquierda)
        derecha = evaluar(nodo.derecha)
        try:
            return nodo.operador.funcion(izquierda, derecha)
        except ZeroDivisionError:
            raise ErrorDeEvaluacion("division entre cero")

    raise ErrorDeEvaluacion(f"nodo desconocido: {nodo!r}")
