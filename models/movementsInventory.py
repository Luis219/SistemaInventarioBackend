from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from config.db import meta, engine

MovimientoInventario = Table(
    "MovimientosInventario",
    meta,
    Column("MovimientoID",Integer, primary_key=True, index=True),
    Column("ProductoID",Integer, ForeignKey("productos.ProductoID")),
    Column("Cantidad",Integer),
    Column("FechaMovimiento",DateTime),
    Column("TipoMovimiento",String(10)),

)

meta.create_all(engine)