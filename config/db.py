from sqlalchemy import create_engine, MetaData
engine= create_engine("mysql+pymysql://root:@localhost:3308/inventario")

meta=MetaData()
try:
    conn = engine.connect()
except SQLAlchemyError as e:
    print(f"Error de conexión a la base de datos: {e}")
