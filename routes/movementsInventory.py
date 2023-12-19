from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, update, delete
from config.db import conn
from models.movementsInventory import MovimientoInventario
from models.products import productos
from schemas.movement import MovimientoInventario as MovimientoInventarioSchema
from fastapi.encoders import jsonable_encoder

movementsInventory = APIRouter()

@movementsInventory.get("/movimientos")
def read_movimientos():
    transaction = conn.begin()
    query = select(
    MovimientoInventario.c.MovimientoID,
    MovimientoInventario.c.ProductoID,
    MovimientoInventario.c.Cantidad,
    MovimientoInventario.c.FechaMovimiento,
    MovimientoInventario.c.TipoMovimiento,
    productos.c.Nombre.label("ProductoNombre")
    ).select_from(MovimientoInventario.join(productos, MovimientoInventario.c.ProductoID == productos.c.ProductoID))
    result = conn.execute(query)
    movimientos_list = result.fetchall()

    transaction.commit()
    transaction.close()

    # Serializar los resultados, incluyendo el nombre de la categoría
    serialized_products = [
        {
            "MovimientoID": movement[0],
            "ProductoID": movement[1],
            "Cantidad": movement[2],
            "FechaMovimiento": movement[3],
            "TipoMovimiento": movement[4],
            "ProductoNombre": movement[5]       
        }
        for movement in movimientos_list
    ]
    

    return serialized_products
    

    serialized_movimientos = [ {"MovimientoID": movement[0], "ProductoID": movement[1], "Cantidad": movement[2], "Fecha": movement[3]}
        for movement in movimientos_list]
    return serialized_movimientos

@movementsInventory.get("/movimientos/{id}")
def get_movement(id: int):
    transaction = conn.begin()
    query = MovimientoInventario.select().where(MovimientoInventario.c.MovimientoID == id)
    result = conn.execute(query)
    movement = result.fetchone()
    transaction.commit()
    transaction.close()
    if movement is None:
        return {"error": "Movimiento no encontrado"}
    else:
        return {"MovimientoID": movement[0], "ProductoID": movement[1], "Cantidad": movement[2], "Fecha": movement[3]}



@movementsInventory.post("/movimientos")
def create_movimiento(movimiento: MovimientoInventarioSchema):
    new_movimiento_data = movimiento.dict()
    transaction = conn.begin()
    try:
        conn.execute(MovimientoInventario.insert().values(new_movimiento_data))
        transaction.commit()
        transaction.close()
    except Exception as e:
        transaction.rollback()
        transaction.close()
        print(f"Error durante la inserción: {e}")

    return {"message": "Movimiento de inventario creado exitosamente", "tipo": movimiento.TipoMovimiento}

@movementsInventory.put("/movimientos/{movimiento_id}")
def update_movimiento(movimiento_id: int, movimiento: MovimientoInventarioSchema):
    updated_movimiento_data = movimiento.dict()
    transaction = conn.begin()
    try:
        conn.execute(MovimientoInventario.update().where(MovimientoInventario.c.MovimientoID == movimiento_id).values(updated_movimiento_data))
        transaction.commit()
        transaction.close()
    except Exception as e:
        transaction.rollback()
        transaction.close()
        print(f"Error durante la actualización: {e}")

    return {"message": "Movimiento de inventario actualizado exitosamente", "movimiento_id": movimiento_id}

@movementsInventory.delete("/movimientos/{movimiento_id}")
def delete_movimiento(movimiento_id: int):
    transaction = conn.begin()
    try:
        conn.execute(MovimientoInventario.delete().where(MovimientoInventario.c.MovimientoID == movimiento_id))
        transaction.commit()
        transaction.close()
    except Exception as e:
        transaction.rollback()
        transaction.close()
        print(f"Error durante la eliminación: {e}")

    return {"message": "Movimiento de inventario eliminado exitosamente", "movimiento_id": movimiento_id}
