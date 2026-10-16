"""Los nodos del arbol de sintaxis abstracta.

Para  3 + 4 * 2  el arbol es:

              OperacionBinaria('+')
              /                   \\
        Numero(3)          OperacionBinaria('*')
                            /                  \\
                      Numero(4)            Numero(2)

Un Numero no contiene nada. Una OperacionBinaria contiene otros nodos, que a
su vez pueden ser numeros u otras operaciones.
"""

from .operadores import Operador


class Nodo:
    """Cualquier cosa que pueda aparecer en el arbol."""


class Numero(Nodo):
    valor: int

    def __init__(self, valor: int) -> None:
        self.valor = valor

    def __repr__(self) -> str:
        return f"Numero({self.valor})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Numero):
            return NotImplemented
        return self.valor == otro.valor


class OperacionBinaria(Nodo):
    operador: Operador
    izquierda: Nodo
    derecha: Nodo

    def __init__(self, operador: Operador, izquierda: Nodo, derecha: Nodo) -> None:
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha

    def __repr__(self) -> str:
        return (f"OperacionBinaria({self.operador.simbolo!r}, "
                f"{self.izquierda!r}, {self.derecha!r})")

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, OperacionBinaria):
            return NotImplemented
        return (self.operador == otro.operador
                and self.izquierda == otro.izquierda
                and self.derecha == otro.derecha)


def formatear_arbol(nodo: Nodo, prefijo: str = "", rama: str = "") -> list[str]:
    """Dibuja el AST como un arbol de texto.

    Sirve para VER como quedo agrupada una expresion, en vez de suponerlo.
    Es la misma idea que el imprimirPorNiveles() de la Practica 3: cuando algo
    no cuadra, lo primero es mirar la estructura.
    """
    if isinstance(nodo, Numero):
        return [prefijo + rama + str(nodo.valor)]

    if not isinstance(nodo, OperacionBinaria):
        raise TypeError(f"nodo desconocido: {nodo!r}")

    lineas = [prefijo + rama + nodo.operador.simbolo]
    if rama == "":
        prefijo_hijos = prefijo
    elif rama.startswith("`"):
        prefijo_hijos = prefijo + "    "
    else:
        prefijo_hijos = prefijo + "|   "

    lineas += formatear_arbol(nodo.izquierda, prefijo_hijos, "|-- ")
    lineas += formatear_arbol(nodo.derecha, prefijo_hijos, "`-- ")
    return lineas
