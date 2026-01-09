from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampedModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: str
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    is_active: bool = True


class Supplier(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    tax_id: str
    contact_name: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    terms: Optional[str] = None
    notes: Optional[str] = None


class Material(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    unit: str
    internal_code: str


class MaterialSupplier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="material.id")
    supplier_id: int = Field(foreign_key="supplier.id")
    supplier_code: Optional[str] = None
    price: float
    currency: str = "EUR"
    lead_time_days: int


class Fabric(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    supplier_id: Optional[int] = Field(default=None, foreign_key="supplier.id")
    color: str
    composition: str
    price_per_meter: float
    supplier_code: str
    internal_code: str


class CustomerFabric(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    meters: float
    labor_cost: float


class SofaModel(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None


class Module(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model_id: int = Field(foreign_key="sofamodel.id")
    name: str = Field(index=True)
    width_cm: float
    depth_cm: float
    height_cm: float
    weight_kg: float


class BillOfMaterials(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    module_id: int = Field(foreign_key="module.id")
    labor_minutes: int
    labor_cost: float


class BomItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bom_id: int = Field(foreign_key="billofmaterials.id")
    material_id: Optional[int] = Field(default=None, foreign_key="material.id")
    fabric_id: Optional[int] = Field(default=None, foreign_key="fabric.id")
    quantity: float
    unit: str


class StockLocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None


class StockItem(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="stocklocation.id")
    material_id: Optional[int] = Field(default=None, foreign_key="material.id")
    module_id: Optional[int] = Field(default=None, foreign_key="module.id")
    product_name: Optional[str] = None
    quantity: float
    unit: str


class Customer(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    billing_address: str
    shipping_address: str
    terms: Optional[str] = None


class SalesOrder(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    status: str = "created"
    currency: str = "EUR"
    total_amount: float = 0


class ProductionOrder(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sales_order_id: Optional[int] = Field(default=None, foreign_key="salesorder.id")
    status: str = "planned"
    priority: int = 3


class ProcessStep(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    production_order_id: int = Field(foreign_key="productionorder.id")
    name: str
    status: str = "pending"
    actual_minutes: Optional[int] = None


class PurchaseOrder(TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    supplier_id: int = Field(foreign_key="supplier.id")
    status: str = "created"
    expected_date: Optional[datetime] = None


class PurchaseOrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    purchase_order_id: int = Field(foreign_key="purchaseorder.id")
    material_id: int = Field(foreign_key="material.id")
    quantity: float
    unit: str
    price: float
    currency: str = "EUR"
