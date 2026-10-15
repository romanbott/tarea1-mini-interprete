"""Pruebas del parser: de los tokens al AST.

Son pruebas unitarias: construimos la lista de `Token` a mano y llamamos
a `Parser(...).parsear()` directamente, sin pasar por el lexer.
Así un defecto del lexer no se confunde con uno del parser.
"""

import pytest

from mini_interprete.ast import Numero, OperacionBinaria
from mini_interprete.errores import ErrorDeSintaxis
from mini_interprete.parser import Parser
from mini_interprete.tokens import TipoToken, Token

# --- Casos normales ---


def test_un_numero_produce_una_hoja():
    tokens = [Token(TipoToken.NUMERO, 42, 0)]
    assert Parser(tokens).parsear() == Numero(42)


def test_la_suma_agrupa_dos_numeros():
    tokens = [
        Token(TipoToken.NUMERO, 3, 0),
        Token(TipoToken.MAS, "+", 1),
        Token(TipoToken.NUMERO, 4, 2),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria("+", Numero(3), Numero(4))


def test_la_resta_agrupa_dos_numeros():
    tokens = [
        Token(TipoToken.NUMERO, 10, 0),
        Token(TipoToken.MENOS, "-", 1),
        Token(TipoToken.NUMERO, 3, 2),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria("-", Numero(10), Numero(3))


def test_el_producto_agrupa_dos_numeros():
    tokens = [
        Token(TipoToken.NUMERO, 6, 0),
        Token(TipoToken.POR, "*", 1),
        Token(TipoToken.NUMERO, 7, 2),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria("*", Numero(6), Numero(7))


def test_la_division_agrupa_dos_numeros():
    tokens = [
        Token(TipoToken.NUMERO, 10, 0),
        Token(TipoToken.ENTRE, "/", 1),
        Token(TipoToken.NUMERO, 2, 2),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria("/", Numero(10), Numero(2))


def test_precedencia_suma_producto():
    # 3 + 4 * 2  debe agruparse como  3 + (4 * 2)
    tokens = [
        Token(TipoToken.NUMERO, 3, 0),
        Token(TipoToken.MAS, "+", 1),
        Token(TipoToken.NUMERO, 4, 2),
        Token(TipoToken.POR, "*", 3),
        Token(TipoToken.NUMERO, 2, 4),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria(
        "+", Numero(3), OperacionBinaria("*", Numero(4), Numero(2))
    )


def test_precedencia_suma_producto_izq():
    # 2 * 3 + 4  debe agruparse como  (2 * 3) + 4
    tokens = [
        Token(TipoToken.NUMERO, 2, 0),
        Token(TipoToken.POR, "*", 1),
        Token(TipoToken.NUMERO, 3, 2),
        Token(TipoToken.MAS, "+", 3),
        Token(TipoToken.NUMERO, 4, 4),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria(
        "+", OperacionBinaria("*", Numero(2), Numero(3)), Numero(4)
    )


def test_los_parentesis_cambian_precedencia():
    # (3 + 4) * 2  debe agruparse al revés que la precedencia normal
    tokens = [
        Token(TipoToken.PAR_IZQ, "(", 0),
        Token(TipoToken.NUMERO, 3, 1),
        Token(TipoToken.MAS, "+", 2),
        Token(TipoToken.NUMERO, 4, 3),
        Token(TipoToken.PAR_DER, ")", 4),
        Token(TipoToken.POR, "*", 5),
        Token(TipoToken.NUMERO, 2, 6),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria(
        "*", OperacionBinaria("+", Numero(3), Numero(4)), Numero(2)
    )


def test_una_operacion_entre_parentesis():
    tokens = [
        Token(TipoToken.PAR_IZQ, "(", 0),
        Token(TipoToken.NUMERO, 3, 1),
        Token(TipoToken.MAS, "+", 2),
        Token(TipoToken.NUMERO, 4, 3),
        Token(TipoToken.PAR_DER, ")", 4),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria("+", Numero(3), Numero(4))


# --- Casos frontera ---


def test_parentesis_anidados():
    tokens = [
        Token(TipoToken.PAR_IZQ, "(", 0),
        Token(TipoToken.PAR_IZQ, "(", 1),
        Token(TipoToken.NUMERO, 3, 2),
        Token(TipoToken.PAR_DER, ")", 3),
        Token(TipoToken.PAR_DER, ")", 4),
    ]
    assert Parser(tokens).parsear() == Numero(3)


def test_anidamiento_profundo():
    # ((2 + 3) * (4 - 1))
    tokens = [
        Token(TipoToken.PAR_IZQ, "(", 0),
        Token(TipoToken.PAR_IZQ, "(", 1),
        Token(TipoToken.NUMERO, 2, 2),
        Token(TipoToken.MAS, "+", 3),
        Token(TipoToken.NUMERO, 3, 4),
        Token(TipoToken.PAR_DER, ")", 5),
        Token(TipoToken.POR, "*", 6),
        Token(TipoToken.PAR_IZQ, "(", 7),
        Token(TipoToken.NUMERO, 4, 8),
        Token(TipoToken.MENOS, "-", 9),
        Token(TipoToken.NUMERO, 1, 10),
        Token(TipoToken.PAR_DER, ")", 11),
        Token(TipoToken.PAR_DER, ")", 12),
    ]
    assert Parser(tokens).parsear() == OperacionBinaria(
        "*",
        OperacionBinaria("+", Numero(2), Numero(3)),
        OperacionBinaria("-", Numero(4), Numero(1)),
    )


# --- Casos invalidos ---


def test_rechaza_una_lista_de_tokens_vacia():
    with pytest.raises(ErrorDeSintaxis):
        Parser([]).parsear()


def test_rechaza_un_token_inesperado_al_inicio():
    tokens = [
        Token(TipoToken.MAS, "+", 0),
        Token(TipoToken.NUMERO, 3, 1),
    ]
    with pytest.raises(ErrorDeSintaxis) as error:
        Parser(tokens).parsear()
    assert error.value.posicion == 0


def test_rechaza_un_parentesis_sin_cerrar():
    tokens = [
        Token(TipoToken.PAR_IZQ, "(", 0),
        Token(TipoToken.NUMERO, 3, 1),
    ]
    with pytest.raises(ErrorDeSintaxis):
        Parser(tokens).parsear()


def test_rechaza_un_operador_sin_operando():
    tokens = [
        Token(TipoToken.NUMERO, 3, 0),
        Token(TipoToken.MAS, "+", 1),
    ]
    with pytest.raises(ErrorDeSintaxis):
        Parser(tokens).parsear()


def test_rechaza_un_parentesis_de_mas():
    tokens = [
        Token(TipoToken.NUMERO, 3, 0),
        Token(TipoToken.PAR_DER, ")", 1),
    ]
    with pytest.raises(ErrorDeSintaxis):
        Parser(tokens).parsear()
