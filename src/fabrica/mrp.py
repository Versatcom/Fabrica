from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Optional


@dataclass(frozen=True)
class RequerimientoMRP:
    item: str
    demanda: int
    stock: int
    requerimiento_neto: int


def _netear_demanda(demanda: int, stock: int) -> int:
    return max(demanda - stock, 0)


def planificar_mrp(
    demanda: Mapping[str, int],
    stock: Mapping[str, int],
    bom: Optional[Mapping[str, Mapping[str, int]]] = None,
) -> Dict[str, RequerimientoMRP]:
    """Calcula requerimientos netos considerando stock disponible y demanda.

    Si se proporciona un BOM (lista de materiales), la demanda de productos terminados
    se expande a componentes.
    """
    requerimientos: Dict[str, RequerimientoMRP] = {}
    demanda_expandida: Dict[str, int] = dict(demanda)

    if bom:
        for producto, cantidad in demanda.items():
            componentes = bom.get(producto, {})
            for componente, cantidad_componente in componentes.items():
                demanda_expandida[componente] = (
                    demanda_expandida.get(componente, 0)
                    + cantidad * cantidad_componente
                )

    for item, cantidad in demanda_expandida.items():
        stock_item = int(stock.get(item, 0))
        neto = _netear_demanda(int(cantidad), stock_item)
        requerimientos[item] = RequerimientoMRP(
            item=item,
            demanda=int(cantidad),
            stock=stock_item,
            requerimiento_neto=neto,
        )

    return requerimientos
