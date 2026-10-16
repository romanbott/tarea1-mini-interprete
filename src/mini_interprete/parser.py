"""De los tokens al AST.

La gramatica que reconoce este parser es:

    expresion := termino  (('+' | '-') termino)*
    termino   := factor   (('*' | '/') factor)*
    factor    := NUMERO | '(' expresion ')'

Los tres niveles son lo que hace que  3 + 4 * 2  se agrupe como  3 + (4 * 2)
y no como  (3 + 4) * 2 : la multiplicacion vive un nivel mas abajo, asi que
se arma primero.
"""

from .ast import Nodo, Numero, OperacionBinaria
from .errores import ErrorDeSintaxis
from .tokens import TipoToken, Token

OPERADORES_SUMA: tuple[TipoToken, TipoToken] = (TipoToken.MAS, TipoToken.MENOS)
OPERADORES_PRODUCTO: tuple[TipoToken, TipoToken] = (TipoToken.POR, TipoToken.ENTRE)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def parsear(self) -> Nodo:
        """Construye el AST de la lista de tokens."""
        nodo = self._expresion()
        sobrante = self._actual()
        if sobrante is not None:
            raise ErrorDeSintaxis(
                f"token inesperado {sobrante.valor!r}", sobrante.posicion
            )
        return nodo

    def _actual(self) -> Token | None:
        """El token en la posicion actual, o None si ya no quedan."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _avanzar(self) -> Token:
        """Consume el token actual y lo regresa."""
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _posicion_final(self) -> int:
        """La posicion justo despues del ultimo token (el final del texto)."""
        if self.tokens:
            return self.tokens[-1].posicion + 1
        return 0

    def _expresion(self) -> Nodo:
        izquierda = self._termino()
        while self._actual() is not None and self._actual().tipo in OPERADORES_SUMA:
            operador = self._avanzar()
            derecha = self._termino()
            izquierda = OperacionBinaria(operador.valor, izquierda, derecha)
        return izquierda

    def _termino(self) -> Nodo:
        izquierda = self._factor()
        while self._actual() is not None and self._actual().tipo in OPERADORES_PRODUCTO:
            operador = self._avanzar()
            derecha = self._factor()
            izquierda = OperacionBinaria(operador.valor, izquierda, derecha)
        return izquierda

    def _factor(self) -> Nodo:
        token = self._actual()
        if token is None:
            raise ErrorDeSintaxis("se esperaba una expresion", self._posicion_final())
        self._avanzar()

        if token.tipo == TipoToken.NUMERO:
            return Numero(token.valor)

        if token.tipo == TipoToken.PAR_IZQ:
            nodo = self._expresion()
            cierre = self._actual()
            if cierre is None:
                raise ErrorDeSintaxis("se esperaba ')'", self._posicion_final())
            if cierre.tipo != TipoToken.PAR_DER:
                raise ErrorDeSintaxis("se esperaba ')'", cierre.posicion)
            self._avanzar()
            return nodo

        raise ErrorDeSintaxis(f"token inesperado {token.valor!r}", token.posicion)
