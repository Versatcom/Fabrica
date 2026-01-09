# Modelo de datos (borrador)

## Entidades principales

### Modelo
- **id** (PK)
- **codigo_interno** (UQ)
- **nombre**
- **descripcion**
- **medidas** (alto/ancho/largo; UQ opcional por combinación)
- **peso_estimado**
- **moneda_id** (FK → Moneda)
- **precio_m2_base**
- **condiciones_comerciales**
- **activo**

### Modulo
- **id** (PK)
- **modelo_id** (FK → Modelo)
- **codigo_interno** (UQ por modelo)
- **nombre**
- **medidas** (alto/ancho/largo)
- **peso_estimado**
- **metraje_estimado**
- **activo**

### Escandallo
- **id** (PK)
- **modulo_id** (FK → Modulo, UQ)
- **version** (UQ por módulo)
- **fecha_vigencia_desde**
- **fecha_vigencia_hasta** (NULL = vigente)
- **notas**

### Tejido
- **id** (PK)
- **codigo_interno** (UQ)
- **codigo_proveedor**
- **nombre**
- **composicion**
- **gramaje**
- **ancho**
- **color**
- **moneda_id** (FK → Moneda)
- **precio_m2**
- **condiciones**
- **activo**

### Material
- **id** (PK)
- **codigo_interno** (UQ)
- **codigo_proveedor**
- **nombre**
- **tipo** (ej. insumo, accesorio, embalaje)
- **unidad_medida_id** (FK → UnidadMedida)
- **peso_unitario**
- **moneda_id** (FK → Moneda)
- **precio_unitario**
- **condiciones**
- **activo**

### Proveedor
- **id** (PK)
- **codigo_interno** (UQ)
- **razon_social**
- **nif_cif** (UQ)
- **email**
- **telefono**
- **direccion_fiscal**
- **moneda_preferida_id** (FK → Moneda)
- **condiciones_pago**
- **activo**

### Cliente
- **id** (PK)
- **codigo_interno** (UQ)
- **razon_social**
- **nif_cif** (UQ)
- **email**
- **telefono**
- **direccion_facturacion**
- **direccion_envio**
- **moneda_preferida_id** (FK → Moneda)
- **condiciones_comerciales**
- **activo**

### Stock
- **id** (PK)
- **ubicacion_id** (FK → Ubicacion)
- **material_id** (FK → Material, NULL si es tejido)
- **tejido_id** (FK → Tejido, NULL si es material)
- **lote**
- **cantidad**
- **unidad_medida_id** (FK → UnidadMedida)
- **metraje**
- **peso**
- **fecha_ultimo_movimiento**

### OrdenVenta
- **id** (PK)
- **numero** (UQ)
- **cliente_id** (FK → Cliente)
- **fecha**
- **estado**
- **moneda_id** (FK → Moneda)
- **importe_total**
- **condiciones**

### OrdenProduccion
- **id** (PK)
- **numero** (UQ)
- **orden_venta_id** (FK → OrdenVenta, UQ si 1:1)
- **modelo_id** (FK → Modelo)
- **cantidad**
- **fecha_inicio**
- **fecha_fin_estimada**
- **estado**

### Proceso
- **id** (PK)
- **orden_produccion_id** (FK → OrdenProduccion)
- **nombre**
- **secuencia**
- **estado**
- **tiempo_estimado**
- **tiempo_real**

### Compra
- **id** (PK)
- **numero** (UQ)
- **proveedor_id** (FK → Proveedor)
- **fecha**
- **moneda_id** (FK → Moneda)
- **importe_total**
- **condiciones**
- **estado**

### Envio
- **id** (PK)
- **numero** (UQ)
- **orden_venta_id** (FK → OrdenVenta)
- **fecha_salida**
- **fecha_entrega_estimada**
- **direccion_envio**
- **transportista**
- **estado**

## Entidades de relación

### MaterialProveedor
- **id** (PK)
- **material_id** (FK → Material)
- **proveedor_id** (FK → Proveedor)
- **codigo_proveedor**
- **precio_unitario**
- **plazo_entrega_dias**
- **moneda_id** (FK → Moneda)
- **condiciones**
- **UQ(material_id, proveedor_id)**

### TejidoProveedor
- **id** (PK)
- **tejido_id** (FK → Tejido)
- **proveedor_id** (FK → Proveedor)
- **codigo_proveedor**
- **precio_m2**
- **plazo_entrega_dias**
- **moneda_id** (FK → Moneda)
- **condiciones**
- **UQ(tejido_id, proveedor_id)**

### OrdenVentaDetalle
- **id** (PK)
- **orden_venta_id** (FK → OrdenVenta)
- **modelo_id** (FK → Modelo)
- **cantidad**
- **precio_unitario**
- **moneda_id** (FK → Moneda)
- **UQ(orden_venta_id, modelo_id)**

### ConsumoEscandallo
- **id** (PK)
- **escandallo_id** (FK → Escandallo)
- **material_id** (FK → Material, NULL si tejido)
- **tejido_id** (FK → Tejido, NULL si material)
- **cantidad**
- **unidad_medida_id** (FK → UnidadMedida)
- **metraje**

## Catálogos auxiliares

### UnidadMedida
- **id** (PK)
- **codigo** (UQ, ej. m, m2, kg, ud)
- **descripcion**

### Moneda
- **id** (PK)
- **codigo** (UQ, ISO 4217)
- **descripcion**
- **simbolo**

### Ubicacion
- **id** (PK)
- **codigo** (UQ)
- **descripcion**
- **tipo** (almacén, tienda, tránsito)

## Relaciones clave
- **Modelo 1 → N Modulo** (Modelo tiene varios módulos).
- **Modulo 1 → 1 Escandallo** (un módulo tiene un escandallo vigente por versión).
- **Material N ↔ N Proveedor** (MaterialProveedor con precio/plazo por proveedor).
- **Tejido N ↔ N Proveedor** (TejidoProveedor con precio/plazo por proveedor).
- **OrdenVenta N → 1 Cliente**.
- **OrdenProduccion 1 → 1 OrdenVenta** (opcional: permitir N:1 si se consolidan OPs por OV).
- **OrdenProduccion 1 → N Proceso**.
- **Stock N → 1 Ubicacion**; **Stock N → 1 Material/Tejido**.

## Claves únicas y reglas de integridad
- **Códigos internos** únicos en cada entidad principal (Modelo, Modulo por modelo, Tejido, Material, Proveedor, Cliente).
- **Número de documentos** únicos: OrdenVenta.numero, OrdenProduccion.numero, Compra.numero, Envio.numero.
- **Integridad de stock**: exactamente uno de `material_id` o `tejido_id` debe estar informado.
- **ConsumoEscandallo**: exactamente uno de `material_id` o `tejido_id` debe estar informado.
- **Precios** siempre asociados a **Moneda**; no permitir precios sin moneda.
- **Metraje/medidas** deben expresar unidad en UnidadMedida cuando aplique.
- **OrdenProduccion ↔ OrdenVenta**: si es 1:1, aplicar UQ(orden_venta_id) en OrdenProduccion.
