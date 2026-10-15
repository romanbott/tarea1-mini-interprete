"""Pruebas del evaluador: de un AST a un número.

Son pruebas unitarias: construimos el AST a mano y llamamos a `evaluar`
directamente, sin pasar por el lexer ni por el parser.
Así un defecto del lexer o del parser no se disfraza de defecto del evaluador,
y podemos probar estados que el pipeline nunca produce (por ejemplo, un operador desconocido).
"""

import pytest

from mini_interprete.ast import Numero, OperacionBinaria
from mini_interprete.errores import ErrorDeEvaluacion
from mini_interprete.evaluator import evaluar

# --- Casos normales ---


def test_un_numero_se_evalua_a_si_mismo():
    assert evaluar(Numero(42)) == 42


def test_suma():
    assert evaluar(OperacionBinaria("+", Numero(3), Numero(7))) == 10


def test_resta():
    assert evaluar(OperacionBinaria("-", Numero(10), Numero(3))) == 7


def test_multiplicacion():
    assert evaluar(OperacionBinaria("*", Numero(6), Numero(7))) == 42


def test_division():
    assert evaluar(OperacionBinaria("/", Numero(10), Numero(2))) == 5.0


def test_operaciones_anidadas():
    # (3 + 4) * 2
    arbol = OperacionBinaria(
        "*", OperacionBinaria("+", Numero(3), Numero(4)), Numero(2)
    )
    assert evaluar(arbol) == 14


# --- Casos frontera ---


def test_division_fraccionaria():
    assert evaluar(OperacionBinaria("/", Numero(10), Numero(4))) == 2.5


def test_division_entre_cero():
    with pytest.raises(ErrorDeEvaluacion):
        evaluar(OperacionBinaria("/", Numero(1), Numero(0)))


def test_division_entre_cero_anidada():
    arbol = OperacionBinaria(
        "+", Numero(1), OperacionBinaria("/", Numero(1), Numero(0))
    )
    with pytest.raises(ErrorDeEvaluacion):
        evaluar(arbol)


# --- Casos inválidos ---


def test_operador_desconocido():
    with pytest.raises(ErrorDeEvaluacion):
        evaluar(OperacionBinaria("@", Numero(1), Numero(2)))


def test_nodo_desconocido():
    with pytest.raises(ErrorDeEvaluacion):
        evaluar("esto no es un nodo")
