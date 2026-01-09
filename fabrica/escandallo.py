from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable, Sequence

from fabrica.tejidos import TejidoBase


@dataclass(frozen=True)
class LineaEscandallo:
    tejido: TejidoBase
    cantidad: Decimal = Decimal("1")

    def coste_total(self) -> Decimal:
        return self.tejido.coste_material() * self.cantidad


@dataclass(frozen=True)
class Escandallo:
    lineas: Sequence[LineaEscandallo] = field(default_factory=tuple)

    def coste_total(self) -> Decimal:
        return sum((linea.coste_total() for linea in self.lineas), Decimal("0"))

    @classmethod
    def desde_tejidos(cls, tejidos: Iterable[TejidoBase]) -> "Escandallo":
        return cls([LineaEscandallo(tejido=tejido) for tejido in tejidos])
