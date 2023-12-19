from fastapi import APIRouter, HTTPException
from config.db import conn,  engine
from models.products import productos
from models.categories import Categoria
from schemas.product import Producto
from sqlalchemy import select
from sqlalchemy.sql.expression import literal_column
from sqlalchemy.orm import sessionmaker
products = APIRouter()


@products.get("/products")
def get_products():
    transaction = conn.begin()
    query = select(
    productos.c.ProductoID,
    productos.c.CategoriaID,
    productos.c.Nombre,
    productos.c.Precio,
    productos.c.Stock,
    Categoria.c.Nombre.label("CategoriaNombre")
    ).select_from(productos.join(Categoria, productos.c.CategoriaID == Categoria.c.CategoriaID))
    result = conn.execute(query)

    productos_con_categorias = result.fetchall()

    transaction.commit()
    transaction.close()
    

    # Serializar los resultados, incluyendo el nombre de la categoría
    serialized_products = [
        {
            "ProductoID": product[0],
            "CategoriaID": product[1],
            "Nombre": product[2],
            "Precio": float(product[3]),
            "Stock": product[4],
            "CategoriaNombre": product[5]
           
        }
        for product in productos_con_categorias
    ]
    
    
    return serialized_products
    

@products.get("/products/{id}")
def get_product(id: int):
    transaction = conn.begin()
    query = productos.select().where(productos.c.ProductoID == id)
    result = conn.execute(query)
    product = result.fetchone()
    transaction.commit()
    transaction.close()
    if product is None:
        
        return {"error": "Producto no encontrado"}
        
    else:
        
        return {"ProductoID": product[0],"CategoriaID": product[1], "Nombre": product[2], "Precio": float(product[3]), "Stock": product[4]}
        
    

@products.post("/products")
def post_products(product: Producto):
    transaction = conn.begin()
    
    # Convertir el objeto Pydantic a un dict
    new_product_data = product.dict()

    # Eliminar el campo "id" si está presente y es None
    if "id" in new_product_data and new_product_data["id"] is None:
        del new_product_data["id"]

    print("Datos a insertar:", new_product_data)

    
    try:
        conn.execute(productos.insert().values(new_product_data))
        transaction.commit()
        transaction.close()
        
    except Exception as e:
        
        print(f"Error durante la inserción: {e}")
    
    return new_product_data
    

@products.put("/products/{product_id}")
def put_product(product_id: int, product: Producto):
    transaction = conn.begin()
    
    # Convertir el objeto Pydantic a un dict
    updated_product_data = product.dict()

    # Eliminar el campo "id" si está presente y es None
    if "id" in updated_product_data and updated_product_data["id"] is None:
        del updated_product_data["id"]

    

    # Actualizar el producto en la base de datos
    stmt = productos.update().where(productos.c.ProductoID == product_id).values(updated_product_data)
    result = conn.execute(stmt)
    transaction.commit()
    transaction.close()
    

    # Verificar si el producto fue actualizado correctamente
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"message": "Producto actualizado exitosamente", "product_id": product_id}
    




@products.delete("/products/{product_id}")
def delete_product(product_id: int):
    # Eliminar el producto de la base de datos
    
    transaction = conn.begin()
    stmt = productos.delete().where(productos.c.ProductoID == product_id)
    result = conn.execute(stmt)
    transaction.commit()
    transaction.close()
    


    # Verificar si el producto fue eliminado correctamente
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"message": "Producto eliminado exitosamente", "product_id": product_id}
    

