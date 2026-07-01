from sqlmodel import SQLModel, Field


class TransaccionBase(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str
    precio_total: float = Field(default=0)


class TransaccionCrear(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str


class TransaccionEditar(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str


class Transaccion(TransaccionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    factura_id: int | None = None