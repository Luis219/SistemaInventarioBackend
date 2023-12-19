from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, update, delete
from config.db import conn
from models.categories import Categoria
from schemas.category import Categoria as CategoriaSchema
from fastapi.encoders import jsonable_encoder

categories = APIRouter()

@categories.get("/categories")
def read_category():
    transaction = conn.begin()
    
    result = conn.execute(Categoria.select())
    categories_list = result.fetchall()
    transaction.commit()
    transaction.close()
    
    serialized_categories = [
        {"CategoriaID": category[0], "Nombre": category[1]}
        for category in categories_list
    ]
    return serialized_categories

@categories.get("/categories/{id}")
def get_category(id: int):
    transaction = conn.begin()
    query = Categoria.select().where(Categoria.c.CategoriaID == id)
    result = conn.execute(query)
    category = result.fetchone()
    transaction.commit()
    transaction.close()
    if category is None:
        return {"error": "Categoría no encontrada"}
    else:
        return {"CategoriaID": category[0], "Nombre": category[1]}

@categories.post("/categories")
def create_category(category: CategoriaSchema):
    new_category_data = category.dict()
  
    transaction = conn.begin()
    try:
        conn.execute(Categoria.insert().values(new_category_data))
        transaction.commit()
        transaction.close()
    except Exception as e:
        transaction.rollback()
        transaction.close()
        print(f"Error durante la inserción: {e}")

    return {"message": "Categoría creada exitosamente", "category_name": category.Nombre}

@categories.put("/categories/{category_id}")
def update_category(category_id: int, category: CategoriaSchema):
   
    updated_category_data = category.dict()
  
    transaction = conn.begin()
    try:
        conn.execute(Categoria.update().where(Categoria.c.CategoriaID == category_id).values(updated_category_data))
        transaction.commit()
        transaction.close()
    except Exception as e:
        transaction.rollback()
        transaction.close()
        print(f"Error durante la actualización: {e}")

    return {"message": "Categoría actualizada exitosamente", "category_id": category_id}

@categories.delete("/categories/{category_id}")
def delete_category(category_id: int):


    transaction = conn.begin()
    try:
        conn.execute(Categoria.delete().where(Categoria.c.CategoriaID == category_id))
        transaction.commit()
        transaction.close()
    except Exception as e:
        transaction.rollback()
        transaction.close()
        print(f"Error durante la eliminación: {e}")

    return {"message": "Categoría eliminada exitosamente", "category_id": category_id}
