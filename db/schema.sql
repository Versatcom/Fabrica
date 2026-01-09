-- Core master data
CREATE TABLE proveedores (
    id BIGSERIAL PRIMARY KEY,
    codigo TEXT UNIQUE,
    razon_social TEXT NOT NULL,
    nombre_comercial TEXT,
    rfc_nif TEXT NOT NULL,
    regimen_fiscal TEXT,
    direccion_fiscal_linea1 TEXT,
    direccion_fiscal_linea2 TEXT,
    ciudad TEXT,
    estado TEXT,
    pais TEXT,
    codigo_postal TEXT,
    contacto_nombre TEXT,
    contacto_email TEXT,
    contacto_telefono TEXT,
    contacto_puesto TEXT,
    condiciones_pago TEXT,
    condiciones_entrega TEXT,
    limite_credito NUMERIC(14, 2),
    moneda_preferida TEXT,
    notas TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE materiales (
    id BIGSERIAL PRIMARY KEY,
    codigo TEXT UNIQUE,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    unidad_medida TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE material_proveedor (
    id BIGSERIAL PRIMARY KEY,
    material_id BIGINT NOT NULL REFERENCES materiales(id) ON DELETE CASCADE,
    proveedor_id BIGINT NOT NULL REFERENCES proveedores(id) ON DELETE CASCADE,
    precio_unitario NUMERIC(14, 4) NOT NULL,
    moneda TEXT NOT NULL,
    plazo_entrega_dias INTEGER,
    cantidad_minima NUMERIC(14, 4),
    cantidad_maxima NUMERIC(14, 4),
    vigente_desde DATE,
    vigente_hasta DATE,
    condiciones_compra TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (material_id, proveedor_id, vigente_desde)
);

-- Purchase orders
CREATE TABLE pedidos_compra (
    id BIGSERIAL PRIMARY KEY,
    numero TEXT UNIQUE NOT NULL,
    proveedor_id BIGINT NOT NULL REFERENCES proveedores(id),
    fecha_emision DATE NOT NULL,
    fecha_entrega_estimada DATE,
    moneda TEXT NOT NULL,
    subtotal NUMERIC(14, 2),
    impuestos NUMERIC(14, 2),
    total NUMERIC(14, 2),
    estado TEXT NOT NULL DEFAULT 'borrador',
    notas TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE pedidos_compra_items (
    id BIGSERIAL PRIMARY KEY,
    pedido_compra_id BIGINT NOT NULL REFERENCES pedidos_compra(id) ON DELETE CASCADE,
    material_id BIGINT NOT NULL REFERENCES materiales(id),
    proveedor_id BIGINT NOT NULL REFERENCES proveedores(id),
    cantidad NUMERIC(14, 4) NOT NULL,
    unidad_medida TEXT,
    precio_unitario NUMERIC(14, 4) NOT NULL,
    moneda TEXT NOT NULL,
    plazo_entrega_dias INTEGER,
    estado TEXT NOT NULL DEFAULT 'pendiente',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Stock and receiving
CREATE TABLE existencias (
    id BIGSERIAL PRIMARY KEY,
    material_id BIGINT NOT NULL UNIQUE REFERENCES materiales(id) ON DELETE CASCADE,
    cantidad_disponible NUMERIC(14, 4) NOT NULL DEFAULT 0,
    cantidad_reservada NUMERIC(14, 4) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE recepciones_compra (
    id BIGSERIAL PRIMARY KEY,
    pedido_compra_id BIGINT NOT NULL REFERENCES pedidos_compra(id),
    proveedor_id BIGINT NOT NULL REFERENCES proveedores(id),
    fecha_recepcion DATE NOT NULL,
    estado TEXT NOT NULL DEFAULT 'recibido',
    notas TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE recepciones_compra_items (
    id BIGSERIAL PRIMARY KEY,
    recepcion_id BIGINT NOT NULL REFERENCES recepciones_compra(id) ON DELETE CASCADE,
    pedido_compra_item_id BIGINT REFERENCES pedidos_compra_items(id),
    material_id BIGINT NOT NULL REFERENCES materiales(id),
    cantidad_recibida NUMERIC(14, 4) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE movimientos_existencias (
    id BIGSERIAL PRIMARY KEY,
    material_id BIGINT NOT NULL REFERENCES materiales(id),
    tipo TEXT NOT NULL,
    referencia TEXT,
    cantidad NUMERIC(14, 4) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION actualizar_existencias_por_recepcion()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO existencias (material_id, cantidad_disponible, updated_at)
    VALUES (NEW.material_id, NEW.cantidad_recibida, NOW())
    ON CONFLICT (material_id)
    DO UPDATE
      SET cantidad_disponible = existencias.cantidad_disponible + NEW.cantidad_recibida,
          updated_at = NOW();

    INSERT INTO movimientos_existencias (material_id, tipo, referencia, cantidad)
    VALUES (NEW.material_id, 'recepcion_compra', NEW.recepcion_id::text, NEW.cantidad_recibida);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_actualizar_existencias_recepcion
AFTER INSERT ON recepciones_compra_items
FOR EACH ROW
EXECUTE FUNCTION actualizar_existencias_por_recepcion();
