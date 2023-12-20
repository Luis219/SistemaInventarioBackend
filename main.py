from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from routes.categories import categories
from routes.products import products
from routes.movementsInventory import movementsInventory
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Configurar CORS
app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)
app.include_router(products)
app.include_router(categories)
app.include_router(movementsInventory)

if __name__ == "__main__":
    import uvicorn

    # Especificar la dirección y el puerto deseado
    uvicorn.run(app, host="0.0.0.0",  debug=True,port=8000, log_level="debug")































"""
class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]

# Lista para almacenar los libros (simulando una base de datos simple)
base_de_datos = []

@app.get("/")
def index():
    
    return {"message": base_de_datos}

@app.get("/libros/{id}")
def mostrarLibro(id: int):
    for libro in base_de_datos:
        if libro["id"] == id:
            return {"data": libro}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/libros")
def insertarLibro(libro: Libro):
    nuevo_libro = {"id": len(base_de_datos) + 1, **libro.dict()}
    base_de_datos.append(nuevo_libro)
    return {"message": f"Libro {libro.titulo} insertado"}

@app.put("/libros/{id}")
def actualizarLibro(id: int, libro: Libro):
    for i, l in enumerate(base_de_datos):
        if l["id"] == id:
            base_de_datos[i] = {"id": id, **libro.dict()}
            return {"message": f"Libro con ID {id} actualizado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/libros/{id}")
def eliminarLibro(id: int):
    for i, libro in enumerate(base_de_datos):
        if libro["id"] == id:
            del base_de_datos[i]
            return {"message": f"Libro con ID {id} eliminado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")
"""