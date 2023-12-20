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

























