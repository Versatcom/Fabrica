"""Inventory domain models for stock types, locations, and movements."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class StockType(str, Enum):
    MATERIA_PRIMA = "MateriaPrima"
    MODULO = "Modulo"
    PRODUCTO_TERMINADO = "ProductoTerminado"


class MovementType(str, Enum):
    ENTRADA = "Entrada"
    SALIDA = "Salida"
    AJUSTE = "Ajuste"


@dataclass(frozen=True)
class Location:
    warehouse: str
    shelf: str

    def label(self) -> str:
        return f"{self.warehouse}/{self.shelf}"


@dataclass
class StockMovement:
    movement_id: str
    stock_type: StockType
    movement_type: MovementType
    quantity: int
    location: Location
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    purchase_id: Optional[str] = None
    production_id: Optional[str] = None
    note: Optional[str] = None

    def link_purchase(self, purchase_id: str) -> None:
        self.purchase_id = purchase_id

    def link_production(self, production_id: str) -> None:
        self.production_id = production_id


@dataclass
class InventoryLedger:
    movements: List[StockMovement] = field(default_factory=list)

    def record_movement(self, movement: StockMovement) -> None:
        self.movements.append(movement)

    def balance_by_location(self) -> Dict[str, int]:
        balances: Dict[str, int] = {}
        for movement in self.movements:
            key = movement.location.label()
            balances.setdefault(key, 0)
            balances[key] += self._signed_quantity(movement)
        return balances

    def balance_by_stock_type(self) -> Dict[StockType, int]:
        balances: Dict[StockType, int] = {}
        for movement in self.movements:
            balances.setdefault(movement.stock_type, 0)
            balances[movement.stock_type] += self._signed_quantity(movement)
        return balances

    def movements_for_purchase(self, purchase_id: str) -> List[StockMovement]:
        return [m for m in self.movements if m.purchase_id == purchase_id]

    def movements_for_production(self, production_id: str) -> List[StockMovement]:
        return [m for m in self.movements if m.production_id == production_id]

    @staticmethod
    def _signed_quantity(movement: StockMovement) -> int:
        if movement.movement_type == MovementType.SALIDA:
            return -movement.quantity
        if movement.movement_type == MovementType.AJUSTE:
            return movement.quantity
        return movement.quantity
