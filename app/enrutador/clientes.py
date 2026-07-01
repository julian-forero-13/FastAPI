from fastapi import APIRouter, HTTPException, status
from app.listas_app import listas_clientes
from app.modelos.clientes import *
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

router = APIRouter(
        prefix="/clientes",
        tags=["Clientes"]
)

@router.get("/", response_model=list[Cliente])
async def listar_cliente(sesion: Sesion_dependencia):
    list_cli = sesion.exec(select(Cliente)).all()
    return list_cli


@router.get("/{id}", response_model=Cliente)
async def listar_cliente_id(id: int, mi_sesion: Sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"El cliente con ID {id}, no existe.")
    return cliente_bd

@router.post("/", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear, mi_sesion: Sesion_dependencia):

    cliente_validado = Cliente.model_validate(
        datos_cliente.model_dump()
    )

    mi_sesion.add(cliente_validado)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_validado)
    return cliente_validado


@router.patch("/{id}", response_model=Cliente)
async def editar_cliente(
    id: int,
    datos_cliente: ClienteEditar,
    mi_sesion: Sesion_dependencia
):
    cliente_bd = mi_sesion.get(Cliente, id)

    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"El cliente con ID {id}, no existe.")
    cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)
    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)
    return cliente_bd

@router.delete("/{id}",  response_model= Cliente)
async def eliminar_cliente(id: int ,mi_sesion: Sesion_dependencia):

    cliente_bd = mi_sesion.get(Cliente, id)

    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"El cliente con ID {id}, no existe.")
    mi_sesion.delete(cliente_bd)
    mi_sesion.commit()
    return cliente_bd