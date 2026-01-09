from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class Contacto:
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    cargo: Optional[str] = None


@dataclass(frozen=True)
class Direccion:
    calle: str
    ciudad: str
    provincia: str
    codigo_postal: str
    pais: str
    instrucciones: Optional[str] = None


@dataclass(frozen=True)
class CondicionesComerciales:
    metodo_pago: str
    plazo_pago_dias: int
    descuento_porcentaje: Decimal = Decimal("0")
    observaciones: Optional[str] = None


@dataclass(frozen=True)
class Moneda:
    codigo: str
    simbolo: str


@dataclass(frozen=True)
class Money:
    importe: Decimal
    moneda: Moneda

    def __add__(self, other: "Money") -> "Money":
        if self.moneda != other.moneda:
            raise ValueError("No se pueden sumar importes con monedas distintas")
        return Money(self.importe + other.importe, self.moneda)

    def __mul__(self, factor: Decimal) -> "Money":
        return Money(self.importe * factor, self.moneda)


@dataclass(frozen=True)
class Cliente:
    identificador: str
    nombre: str
    contactos: List[Contacto] = field(default_factory=list)
    direcciones: List[Direccion] = field(default_factory=list)
    condiciones: Optional[CondicionesComerciales] = None
    direccion_envio: Optional[Direccion] = None


@dataclass(frozen=True)
class LineaOrdenVenta:
    sku: str
    descripcion: str
    cantidad: int
    precio_unitario: Money

    def total(self) -> Money:
        return self.precio_unitario * Decimal(self.cantidad)


class EstadoOrdenVenta(str, Enum):
    CREADO = "creado"
    EN_PRODUCCION = "en_produccion"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


@dataclass
class OrdenVenta:
    numero: str
    cliente: Cliente
    moneda: Moneda
    fecha: date = field(default_factory=date.today)
    estado: EstadoOrdenVenta = EstadoOrdenVenta.CREADO
    lineas: List[LineaOrdenVenta] = field(default_factory=list)

    def agregar_linea(self, linea: LineaOrdenVenta) -> None:
        if linea.precio_unitario.moneda != self.moneda:
            raise ValueError("La moneda de la linea no coincide con la moneda del pedido")
        self.lineas.append(linea)

    def total(self) -> Money:
        total = Money(Decimal("0"), self.moneda)
        for linea in self.lineas:
            total = total + linea.total()
        return total

    def actualizar_estado(self, nuevo_estado: EstadoOrdenVenta) -> None:
        self.estado = nuevo_estado

    def lineas_enviables(self) -> Iterable[LineaOrdenVenta]:
        return list(self.lineas)
