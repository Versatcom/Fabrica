from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional

from fabrica.validation import (
    is_email,
    is_non_empty,
    is_optional_phone,
    is_positive_number,
)

Validator = Callable[[str], bool]


@dataclass(frozen=True)
class TemplateField:
    name: str
    required: bool = True
    validator: Optional[Validator] = None
    description: str = ""


@dataclass(frozen=True)
class ImportTemplate:
    key: str
    label: str
    fields: List[TemplateField]

    def header(self) -> List[str]:
        return [field.name for field in self.fields]

    def required_fields(self) -> List[str]:
        return [field.name for field in self.fields if field.required]


def _fabric_template() -> ImportTemplate:
    return ImportTemplate(
        key="tejidos",
        label="Tejidos",
        fields=[
            TemplateField("codigo", validator=is_non_empty, description="SKU interno"),
            TemplateField("nombre", validator=is_non_empty),
            TemplateField("tipo", validator=is_non_empty),
            TemplateField("ancho_cm", validator=is_positive_number),
            TemplateField("peso_gm2", validator=is_positive_number),
            TemplateField("color", required=False),
            TemplateField("proveedor", required=False),
        ],
    )


def _material_template() -> ImportTemplate:
    return ImportTemplate(
        key="materiales",
        label="Materiales",
        fields=[
            TemplateField("codigo", validator=is_non_empty),
            TemplateField("nombre", validator=is_non_empty),
            TemplateField("categoria", validator=is_non_empty),
            TemplateField("unidad_medida", validator=is_non_empty),
            TemplateField("costo_unitario", validator=is_positive_number),
            TemplateField("proveedor", required=False),
        ],
    )


def _supplier_template() -> ImportTemplate:
    return ImportTemplate(
        key="proveedores",
        label="Proveedores",
        fields=[
            TemplateField("razon_social", validator=is_non_empty),
            TemplateField("identificacion", validator=is_non_empty),
            TemplateField("email", required=False, validator=is_email),
            TemplateField("telefono", required=False, validator=is_optional_phone),
            TemplateField("direccion", required=False),
            TemplateField("ciudad", required=False),
            TemplateField("pais", required=False),
        ],
    )


def _customer_template() -> ImportTemplate:
    return ImportTemplate(
        key="clientes",
        label="Clientes",
        fields=[
            TemplateField("razon_social", validator=is_non_empty),
            TemplateField("identificacion", validator=is_non_empty),
            TemplateField("email", required=False, validator=is_email),
            TemplateField("telefono", required=False, validator=is_optional_phone),
            TemplateField("direccion", required=False),
            TemplateField("ciudad", required=False),
            TemplateField("pais", required=False),
            TemplateField("segmento", required=False),
        ],
    )


_TEMPLATES: Dict[str, ImportTemplate] = {
    "tejidos": _fabric_template(),
    "materiales": _material_template(),
    "proveedores": _supplier_template(),
    "clientes": _customer_template(),
}


def list_templates() -> Iterable[ImportTemplate]:
    return _TEMPLATES.values()


def get_template(key: str) -> ImportTemplate:
    normalized = key.strip().lower()
    if normalized not in _TEMPLATES:
        available = ", ".join(sorted(_TEMPLATES))
        raise KeyError(f"Plantilla desconocida: {key}. Disponibles: {available}")
    return _TEMPLATES[normalized]
