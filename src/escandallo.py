from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class MaterialRule:
    material_type: str

    def calculate_quantity(self, measurements: Dict[str, float], material: "MaterialItem") -> float:
        raise NotImplementedError


@dataclass
class FabricRule(MaterialRule):
    roll_width: float

    def calculate_quantity(self, measurements: Dict[str, float], material: "MaterialItem") -> float:
        width = measurements.get("width", 0)
        height = measurements.get("height", 0)
        depth = measurements.get("depth", 0)
        seam_allowance = material.metadata.get("seam_allowance", 0)
        layers = material.metadata.get("layers", 1)
        surface_area = (width + seam_allowance) * (height + seam_allowance)
        side_area = (depth + seam_allowance) * (height + seam_allowance)
        total_area = (surface_area + side_area) * layers
        return total_area / max(self.roll_width, 1)


@dataclass
class FillingRule(MaterialRule):
    density: float

    def calculate_quantity(self, measurements: Dict[str, float], material: "MaterialItem") -> float:
        width = measurements.get("width", 0)
        height = measurements.get("height", 0)
        depth = measurements.get("depth", 0)
        volume = width * height * depth
        return (volume * self.density) / 1000


@dataclass
class MaterialItem:
    name: str
    material_type: str
    unit_cost: float
    quantity: float = 0
    metadata: Dict[str, float] = field(default_factory=dict)

    @property
    def total_cost(self) -> float:
        return self.unit_cost * self.quantity


@dataclass
class LaborItem:
    name: str
    hourly_rate: float
    hours: float

    @property
    def total_cost(self) -> float:
        return self.hourly_rate * self.hours


@dataclass
class HardwareItem:
    name: str
    unit_cost: float
    quantity: float

    @property
    def total_cost(self) -> float:
        return self.unit_cost * self.quantity


@dataclass
class TimeEntry:
    name: str
    minutes: float


@dataclass
class EscandalloSnapshot:
    timestamp: datetime
    reason: str
    data: Dict[str, object]


@dataclass
class Escandallo:
    module_id: str
    measurements: Dict[str, float]
    materials: List[MaterialItem] = field(default_factory=list)
    labor: List[LaborItem] = field(default_factory=list)
    hardware: List[HardwareItem] = field(default_factory=list)
    times: List[TimeEntry] = field(default_factory=list)
    rules: Dict[str, MaterialRule] = field(default_factory=dict)
    history: List[EscandalloSnapshot] = field(default_factory=list)

    def recalculate(self, reason: str = "recalculated") -> None:
        for material in self.materials:
            rule = self.rules.get(material.material_type)
            if rule:
                material.quantity = rule.calculate_quantity(self.measurements, material)
        self._add_snapshot(reason)

    def update_measurements(self, updates: Dict[str, float]) -> None:
        self.measurements.update(updates)
        self.recalculate("measurements updated")

    def update_material(
        self,
        name: str,
        unit_cost: Optional[float] = None,
        metadata: Optional[Dict[str, float]] = None,
    ) -> None:
        for material in self.materials:
            if material.name == name:
                if unit_cost is not None:
                    material.unit_cost = unit_cost
                if metadata is not None:
                    material.metadata.update(metadata)
                self.recalculate(f"material updated: {name}")
                return
        raise ValueError(f"Material '{name}' not found")

    def total_material_cost(self) -> float:
        return sum(material.total_cost for material in self.materials)

    def total_labor_cost(self) -> float:
        return sum(item.total_cost for item in self.labor)

    def total_hardware_cost(self) -> float:
        return sum(item.total_cost for item in self.hardware)

    def total_cost(self) -> float:
        return self.total_material_cost() + self.total_labor_cost() + self.total_hardware_cost()

    def _add_snapshot(self, reason: str) -> None:
        self.history.append(
            EscandalloSnapshot(
                timestamp=datetime.utcnow(),
                reason=reason,
                data=self.to_dict(),
            )
        )

    def to_dict(self) -> Dict[str, object]:
        return {
            "module_id": self.module_id,
            "measurements": dict(self.measurements),
            "materials": [
                {
                    "name": material.name,
                    "material_type": material.material_type,
                    "unit_cost": material.unit_cost,
                    "quantity": material.quantity,
                    "metadata": dict(material.metadata),
                    "total_cost": material.total_cost,
                }
                for material in self.materials
            ],
            "labor": [
                {
                    "name": item.name,
                    "hourly_rate": item.hourly_rate,
                    "hours": item.hours,
                    "total_cost": item.total_cost,
                }
                for item in self.labor
            ],
            "hardware": [
                {
                    "name": item.name,
                    "unit_cost": item.unit_cost,
                    "quantity": item.quantity,
                    "total_cost": item.total_cost,
                }
                for item in self.hardware
            ],
            "times": [{"name": entry.name, "minutes": entry.minutes} for entry in self.times],
            "total_cost": self.total_cost(),
        }
