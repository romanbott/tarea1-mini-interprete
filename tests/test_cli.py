"""Pruebas de la linea de comandos.

Se prueban el despacho de banderas, los comandos, los
codigos de salida y el flujo de entrada.
"""

import io

import pytest

from mini_interprete.cli import _ejecutar, _elegir_comando, _procesar_entrada, main
from mini_interprete.comandos import COMANDOS
from mini_interprete.errores import ErrorDeComando

# --- Despacho de banderas ---


def test_sin_bandera_se_evalua():
    assert _elegir_comando(["3 + 4"]) == ("evaluar", ["3 + 4"])


def test_la_bandera_arbol_selecciona_su_comando():
    assert _elegir_comando(["--arbol", "3 + 4"]) == ("arbol", ["3 + 4"])


def test_la_bandera_puede_ir_despues_de_la_expresion():
    assert _elegir_comando(["3 + 4", "--arbol"]) == ("arbol", ["3 + 4"])


def test_una_bandera_inexistente_falla():
    with pytest.raises(ErrorDeComando) as error:
        _elegir_comando(["--comando_inexistente", "3 + 4"])
    assert "comando" in str(error.value).lower()


# --- Comandos ---


def test_el_comando_evaluar():
    assert COMANDOS["evaluar"]("3 + 4") == "7"


def test_el_comando_arbol():
    assert COMANDOS["arbol"]("3 + 4").splitlines() == ["+", "|-- 3", "`-- 4"]


# --- Codigos de salida ---


def test_main_evalua_y_sale_con_cero():
    assert main(["3 + 4"]) == 0


def test_una_expresion_invalida_sale_con_uno():
    assert _ejecutar("evaluar", "3 @") == 1


def test_el_modo_interactivo_propaga_el_error():
    assert _procesar_entrada("evaluar", io.StringIO("3 + 4\n3 @\n")) == 1
