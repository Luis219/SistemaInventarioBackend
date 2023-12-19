from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Numeric, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.db import meta, engine

Categoria = Table(
    "categorias",
    meta,
    Column("CategoriaID", Integer, primary_key=True, index=True),
    Column("Nombre", String(100), index=True),
)

meta.create_all(engine)