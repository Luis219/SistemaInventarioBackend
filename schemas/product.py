from typing import Optional
from pydantic import BaseModel

class Producto(BaseModel):
      CategoriaID: int
      Nombre: str
      Precio: float
      Stock: int