from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..conexion_bd import Sesion_dependencia
from app.modelos.transacciones import *
from app.modelos.factura import Factura

router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)

@router.get("/")
async def listar_transacciones(mi_sesion: Sesion_dependencia):

    transacciones = mi_sesion.exec(select(Transaccion)).all()
    return transacciones

@router.get("/{id}")
async def obtener_transaccion(
    id: int,
    mi_sesion: Sesion_dependencia
):
    
    transaccion = mi_sesion.get(Transaccion, id)

    if not transaccion:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    return transaccion
    
@router.post("/{factura_id}")
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear,
    mi_sesion: Sesion_dependencia
):

    factura_encontrada = mi_sesion.get(Factura, factura_id)

    if not factura_encontrada:

        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    transaccion = Transaccion.model_validate(
        datos_transaccion.model_dump()
    )

    transaccion.factura_id = factura_id
    transaccion.precio_total = transaccion.cantidad * transaccion.vr_unitario

    mi_sesion.add(transaccion)
    mi_sesion.commit()
    mi_sesion.refresh(transaccion)

    return transaccion

@router.put("/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionEditar,
    mi_sesion: Sesion_dependencia
):

    transaccion = mi_sesion.get(Transaccion, id)

    if not transaccion:

        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    datos = datos_transaccion.model_dump(exclude_unset=True)

    transaccion.sqlmodel_update(datos)

    mi_sesion.add(transaccion)
    mi_sesion.commit()
    mi_sesion.refresh(transaccion)

    return transaccion

@router.delete("/{id}")
async def eliminar_transaccion(
    id: int,
    mi_sesion: Sesion_dependencia
):

    transaccion = mi_sesion.get(Transaccion, id)

    if not transaccion:

        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    mi_sesion.delete(transaccion)
    mi_sesion.commit()

    return transaccion