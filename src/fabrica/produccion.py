from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Iterable, List, Optional


class Estacion(str, Enum):
    CORTE = "corte"
    COSTURA = "costura"
    TAPIZADO = "tapizado"
    EMBALAJE = "embalaje"


class EstadoEstacion(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    COMPLETADO = "completado"


@dataclass(frozen=True)
class Modulo:
    sku: str
    descripcion: str
    cantidad: int


@dataclass(frozen=True)
class Pedido:
    id_pedido: str
    cliente: str
    modulos: List[Modulo]


@dataclass
class RegistroEstacion:
    estacion: Estacion
    estado: EstadoEstacion = EstadoEstacion.PENDIENTE
    inicio_real: Optional[datetime] = None
    fin_real: Optional[datetime] = None

    def iniciar(self, momento: Optional[datetime] = None) -> None:
        if self.estado == EstadoEstacion.COMPLETADO:
            raise ValueError("La estación ya está completada.")
        self.estado = EstadoEstacion.EN_PROCESO
        self.inicio_real = momento or datetime.utcnow()

    def completar(self, momento: Optional[datetime] = None) -> None:
        if self.estado == EstadoEstacion.PENDIENTE:
            raise ValueError("No se puede completar una estación pendiente.")
        self.estado = EstadoEstacion.COMPLETADO
        self.fin_real = momento or datetime.utcnow()

    @property
    def tiempo_real(self) -> Optional[timedelta]:
        if self.inicio_real and self.fin_real:
            return self.fin_real - self.inicio_real
        return None


@dataclass
class OrdenProduccion:
    id_orden: str
    pedido: Pedido
    estaciones: Dict[Estacion, RegistroEstacion] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.estaciones:
            self.estaciones = {
                estacion: RegistroEstacion(estacion=estacion)
                for estacion in Estacion
            }

    @property
    def modulos(self) -> List[Modulo]:
        return list(self.pedido.modulos)

    def obtener_estado_estaciones(self) -> Dict[Estacion, EstadoEstacion]:
        return {
            estacion: registro.estado for estacion, registro in self.estaciones.items()
        }

    def registrar_inicio(self, estacion: Estacion, momento: Optional[datetime] = None) -> None:
        self.estaciones[estacion].iniciar(momento=momento)

    def registrar_fin(self, estacion: Estacion, momento: Optional[datetime] = None) -> None:
        self.estaciones[estacion].completar(momento=momento)

    def tiempos_reales(self) -> Dict[Estacion, Optional[timedelta]]:
        return {
            estacion: registro.tiempo_real
            for estacion, registro in self.estaciones.items()
        }


def crear_orden_produccion(
    id_orden: str, pedido: Pedido, estaciones: Optional[Iterable[Estacion]] = None
) -> OrdenProduccion:
    registros = (
        {
            estacion: RegistroEstacion(estacion=estacion)
            for estacion in estaciones
        }
        if estaciones
        else None
    )
    return OrdenProduccion(id_orden=id_orden, pedido=pedido, estaciones=registros or {})
