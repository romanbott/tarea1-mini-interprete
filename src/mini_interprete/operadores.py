"""El catalogo de operadores.

Aquí se centraliza la información sobre los operadores:
su simbolo, su precedencia y la operacion que calculan.
El parser construye los nodos con un `Operador` y el evaluador lo resuelve a partir de el,
en vez de comparar cadenas sueltas.
"""

import operator
from collections.abc import Callable
from enum import Enum


class Operador(Enum):
    SUMA = ("+", 1, operator.add)
    RESTA = ("-", 1, operator.sub)
    PRODUCTO = ("*", 2, operator.mul)
    COCIENTE = ("/", 2, operator.truediv)

    simbolo: str
    precedencia: int
    funcion: Callable[[int | float, int | float], int | float]

    def __init__(
        self,
        simbolo: str,
        precedencia: int,
        funcion: Callable[[int | float, int | float], int | float],
    ) -> None:
        self.simbolo = simbolo
        self.precedencia = precedencia
        self.funcion = funcion

    @classmethod
    def de_simbolo(cls, simbolo: str) -> "Operador":
        """El operador que se escribe con ese simbolo. Falla si no existe."""
        if simbolo not in POR_SIMBOLO:
            raise ValueError(f"operador desconocido: {simbolo!r}")
        return POR_SIMBOLO[simbolo]


# Para reconocer un operador a partir del texto, sin excepciones de control.
POR_SIMBOLO: dict[str, Operador] = {operador.simbolo: operador for operador in Operador}
