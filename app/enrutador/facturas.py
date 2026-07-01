from fastapi import APIRouter, HTTPException
from app.modelos.factura import Factura, CrearFactura, EditarFactura
from app.modelos.clientes import Cliente
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select


router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)


@router.get("/", response_model=list[Factura])
async def listar_facturas(mi_sesion: Sesion_dependencia):

    facturas = mi_sesion.exec(select(Factura)).all()

    return facturas


@router.get("/{id}", response_model=Factura)
async def obtener_factura(
    id: int,
    mi_sesion: Sesion_dependencia
):

    factura = mi_sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    return factura


@router.post("/{cliente_id}", response_model=Factura)
async def crear_factura(
    cliente_id: int,
    datos_factura: CrearFactura,
    mi_sesion: Sesion_dependencia
):

    cliente_encontrado = mi_sesion.get(Cliente, cliente_id)

    if not cliente_encontrado:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    datos = datos_factura.model_dump()

    # Se agrega solamente una vez el cliente_id
    datos["cliente_id"] = cliente_id

    factura = Factura.model_validate(datos)

    mi_sesion.add(factura)
    mi_sesion.commit()
    mi_sesion.refresh(factura)

    return factura


@router.put("/{id}", response_model=Factura)
async def editar_factura(
    id: int,
    datos_factura: EditarFactura,
    mi_sesion: Sesion_dependencia
):

    factura = mi_sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    datos = datos_factura.model_dump(exclude_unset=True)

    factura.sqlmodel_update(datos)

    mi_sesion.add(factura)
    mi_sesion.commit()
    mi_sesion.refresh(factura)

    return factura


@router.delete("/{id}", response_model=Factura)
async def eliminar_factura(
    id: int,
    mi_sesion: Sesion_dependencia
):

    factura = mi_sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    mi_sesion.delete(factura)
    mi_sesion.commit()

    return factura