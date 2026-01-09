from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Sequence


@dataclass(frozen=True)
class TejidoBase:
    """Base para tejidos con metraje asociado."""

    metraje: Decimal

    def coste_material(self) -> Decimal:
        raise NotImplementedError


@dataclass(frozen=True)
class Tejido(TejidoBase):
    """Tejido estándar con proveedor, composición y precio por metro."""

    proveedor: str
    color: str
    composicion: str
    precio_metro: Decimal
    codigos: Sequence[str] = field(default_factory=tuple)

    def coste_material(self) -> Decimal:
        return self.metraje * self.precio_metro


@dataclass(frozen=True)
class TejidoCliente(TejidoBase):
    """Tejido aportado por cliente con un coste fijo de mano de obra."""

    precio_fijo_mano_obra: Decimal

    def coste_material(self) -> Decimal:
        return self.precio_fijo_mano_obra
