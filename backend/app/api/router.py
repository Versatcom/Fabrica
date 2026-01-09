from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import (
    Customer,
    Fabric,
    Material,
    Module,
    ProductionOrder,
    SalesOrder,
    SofaModel,
    StockItem,
    StockLocation,
    Supplier,
)

router = APIRouter()


def get_or_404(session: Session, model, item_id: int):
    item = session.get(model, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/models", response_model=list[SofaModel])
def list_models(session: Session = Depends(get_session)):
    return session.exec(select(SofaModel)).all()


@router.post("/models", response_model=SofaModel)
def create_model(model: SofaModel, session: Session = Depends(get_session)):
    session.add(model)
    session.commit()
    session.refresh(model)
    return model


@router.get("/modules", response_model=list[Module])
def list_modules(session: Session = Depends(get_session)):
    return session.exec(select(Module)).all()


@router.post("/modules", response_model=Module)
def create_module(module: Module, session: Session = Depends(get_session)):
    session.add(module)
    session.commit()
    session.refresh(module)
    return module


@router.get("/fabrics", response_model=list[Fabric])
def list_fabrics(session: Session = Depends(get_session)):
    return session.exec(select(Fabric)).all()


@router.post("/fabrics", response_model=Fabric)
def create_fabric(fabric: Fabric, session: Session = Depends(get_session)):
    session.add(fabric)
    session.commit()
    session.refresh(fabric)
    return fabric


@router.get("/materials", response_model=list[Material])
def list_materials(session: Session = Depends(get_session)):
    return session.exec(select(Material)).all()


@router.post("/materials", response_model=Material)
def create_material(material: Material, session: Session = Depends(get_session)):
    session.add(material)
    session.commit()
    session.refresh(material)
    return material


@router.get("/suppliers", response_model=list[Supplier])
def list_suppliers(session: Session = Depends(get_session)):
    return session.exec(select(Supplier)).all()


@router.post("/suppliers", response_model=Supplier)
def create_supplier(supplier: Supplier, session: Session = Depends(get_session)):
    session.add(supplier)
    session.commit()
    session.refresh(supplier)
    return supplier


@router.get("/customers", response_model=list[Customer])
def list_customers(session: Session = Depends(get_session)):
    return session.exec(select(Customer)).all()


@router.post("/customers", response_model=Customer)
def create_customer(customer: Customer, session: Session = Depends(get_session)):
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get("/sales-orders", response_model=list[SalesOrder])
def list_sales_orders(session: Session = Depends(get_session)):
    return session.exec(select(SalesOrder)).all()


@router.post("/sales-orders", response_model=SalesOrder)
def create_sales_order(order: SalesOrder, session: Session = Depends(get_session)):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.get("/production-orders", response_model=list[ProductionOrder])
def list_production_orders(session: Session = Depends(get_session)):
    return session.exec(select(ProductionOrder)).all()


@router.post("/production-orders", response_model=ProductionOrder)
def create_production_order(
    order: ProductionOrder, session: Session = Depends(get_session)
):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.get("/stock-locations", response_model=list[StockLocation])
def list_stock_locations(session: Session = Depends(get_session)):
    return session.exec(select(StockLocation)).all()


@router.post("/stock-locations", response_model=StockLocation)
def create_stock_location(
    location: StockLocation, session: Session = Depends(get_session)
):
    session.add(location)
    session.commit()
    session.refresh(location)
    return location


@router.get("/stock-items", response_model=list[StockItem])
def list_stock_items(session: Session = Depends(get_session)):
    return session.exec(select(StockItem)).all()


@router.post("/stock-items", response_model=StockItem)
def create_stock_item(item: StockItem, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
