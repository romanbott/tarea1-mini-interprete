"""Las piezas en las que el lexer parte el texto."""

from enum import Enum


class TipoToken(Enum):
    NUMERO = "NUMERO"
    MAS = "MAS"
    MENOS = "MENOS"
    POR = "POR"
    ENTRE = "ENTRE"
    PAR_IZQ = "PAR_IZQ"
    PAR_DER = "PAR_DER"


class Token:
    """Un token sabe que es, que valor tiene y en que posicion del texto estaba.

    La posicion sirve para que los mensajes de error puedan senalar el lugar
    exacto donde algo salio mal.
    """

    tipo: TipoToken
    valor: int | str
    posicion: int

    def __init__(self, tipo: TipoToken, valor: int | str, posicion: int) -> None:
        self.tipo = tipo
        self.valor = valor
        self.posicion = posicion

    def __repr__(self) -> str:
        return f"Token({self.tipo.name}, {self.valor!r}, {self.posicion})"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Token):
            return NotImplemented
        return (self.tipo == otro.tipo
                and self.valor == otro.valor
                and self.posicion == otro.posicion)


def formatear_tokens(tokens: list[Token]) -> list[str]:
    """Una linea de texto por token."""
    return [repr(token) for token in tokens]
