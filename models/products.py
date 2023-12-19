from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Numeric, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from config.db import meta, engine

productos = Table(
    "productos",
    meta,
    Column("ProductoID", Integer, primary_key=True, index=True),
    Column("CategoriaID",Integer, ForeignKey("categorias.CategoriaID")),
    Column("Nombre", String(100)),
    Column("Precio", Numeric(10, 2)),
    Column("Stock", Integer),
)

meta.create_all(engine)