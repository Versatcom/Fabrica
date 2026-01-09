from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from fabrica.escandallo import Escandallo


@dataclass(frozen=True)
class OrdenVenta:
    referencia: str
    escandallo: Escandallo

    def coste_materiales(self) -> Decimal:
        return self.escandallo.coste_total()


@dataclass(frozen=True)
class OrdenProduccion:
    referencia: str
    escandallo: Escandallo

    def coste_materiales(self) -> Decimal:
        return self.escandallo.coste_total()
