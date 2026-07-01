from datetime import datetime
from sqlmodel import SQLModel, Field


class FacturaBase(SQLModel):
    cliente_id: int = Field(foreign_key="cliente.id")
    fecha: datetime


class CrearFactura(SQLModel):
    fecha: datetime


class EditarFactura(SQLModel):
    fecha: datetime


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)