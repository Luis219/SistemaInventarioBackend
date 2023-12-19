
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MovimientoInventario(BaseModel):
    ProductoID: int
    Cantidad: int
    FechaMovimiento: datetime
    TipoMovimiento: str
