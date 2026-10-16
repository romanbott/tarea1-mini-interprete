"""Linea de comandos del interprete.

python3 interprete.py "3 + 4 * 2"            evalua (por defecto)
python3 interprete.py --arbol "3 + 4 * 2"    dibuja el AST
python3 interprete.py --tokenizar "3 + 4"    muestra los tokens
python3 interprete.py --parsear "3 + 4"      muestra el AST
python3 interprete.py                        (interactivo, Ctrl-D para salir)
"""

import sys
from collections.abc import Iterable

from .comandos import COMANDOS
from .errores import ErrorDeComando, ErrorDelInterprete

# Cada bandera elige un comando; sin bandera se evalua.
BANDERAS: dict[str, str] = {
    "--arbol": "arbol",
    "--tokenizar": "tokenizar",
    "--parsear": "parsear",
}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        comando, argv = _elegir_comando(argv)
    except ErrorDeComando as error:
        return _reportar(error)

    if argv:
        return _ejecutar(comando, " ".join(argv))

    return _procesar_entrada(comando, sys.stdin)


def _procesar_entrada(comando: str, flujo: Iterable[str]) -> int:
    """Corre el comando sobre cada linea de la entrada."""
    codigo = 0
    for linea in flujo:
        linea = linea.strip()
        if linea and _ejecutar(comando, linea):
            codigo = 1
    return codigo


def _elegir_comando(argv: list[str]) -> tuple[str, list[str]]:
    """Separa la bandera (si la hay) del texto de la expresion."""
    comando = "evaluar"
    resto = []
    for arg in argv:
        if arg in BANDERAS:
            comando = BANDERAS[arg]
        elif arg.startswith("--"):
            raise ErrorDeComando(f"comando no encontrado: {arg!r}")
        else:
            resto.append(arg)
    return comando, resto


def _ejecutar(comando: str, texto: str) -> int:
    """Corre el comando, imprime su salida y regresa el codigo de salida."""
    try:
        print(COMANDOS[comando](texto))
        return 0
    except ErrorDelInterprete as error:
        return _reportar(error)


def _reportar(error: ErrorDelInterprete) -> int:
    """Imprime el error en stderr y regresa el codigo de fallo."""
    print(f"Error: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
