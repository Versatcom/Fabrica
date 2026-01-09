from __future__ import annotations

from datetime import date
from typing import Iterable

from .models import Cliente, Direccion, LineaOrdenVenta, Money, OrdenVenta


def _formatear_direccion(direccion: Direccion) -> str:
    instrucciones = f"\nInstrucciones: {direccion.instrucciones}" if direccion.instrucciones else ""
    return (
        f"{direccion.calle}\n"
        f"{direccion.codigo_postal} {direccion.ciudad} ({direccion.provincia})\n"
        f"{direccion.pais}{instrucciones}"
    )


def _formatear_importe(importe: Money) -> str:
    return f"{importe.moneda.simbolo}{importe.importe:.2f} {importe.moneda.codigo}"


def generar_etiqueta(cliente: Cliente, direccion_envio: Direccion) -> str:
    return (
        "ETIQUETA DE ENVIO\n"
        f"Cliente: {cliente.nombre}\n"
        f"Destino:\n{_formatear_direccion(direccion_envio)}\n"
    )


def generar_albaran(orden: OrdenVenta) -> str:
    lineas = "\n".join(
        f"- {linea.sku} | {linea.descripcion} | {linea.cantidad}"
        for linea in orden.lineas_enviables()
    )
    direccion_envio = orden.cliente.direccion_envio
    if direccion_envio is None:
        raise ValueError("La orden no tiene direccion de envio configurada")
    return (
        "ALBARAN\n"
        f"Orden: {orden.numero}\n"
        f"Fecha: {orden.fecha.isoformat()}\n"
        f"Cliente: {orden.cliente.nombre}\n"
        f"Direccion envio:\n{_formatear_direccion(direccion_envio)}\n"
        "Lineas:\n"
        f"{lineas}\n"
    )


def generar_factura(orden: OrdenVenta, fecha_emision: date) -> str:
    total = orden.total()
    lineas = "\n".join(
        f"- {linea.descripcion}: {linea.cantidad} x "
        f"{_formatear_importe(linea.precio_unitario)}"
        for linea in orden.lineas
    )
    return (
        "FACTURA\n"
        f"Orden: {orden.numero}\n"
        f"Fecha emision: {fecha_emision.isoformat()}\n"
        f"Cliente: {orden.cliente.nombre}\n"
        "Lineas:\n"
        f"{lineas}\n"
        f"Total: {_formatear_importe(total)}\n"
    )


def generar_documentos(orden: OrdenVenta, fecha_emision: date) -> Iterable[str]:
    direccion_envio = orden.cliente.direccion_envio
    if direccion_envio is None:
        raise ValueError("La orden no tiene direccion de envio configurada")
    return (
        generar_etiqueta(orden.cliente, direccion_envio),
        generar_albaran(orden),
        generar_factura(orden, fecha_emision),
    )
