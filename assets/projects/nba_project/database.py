# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Construir la URL de conexión
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# El Engine con Pool de conexiones (evita que los scripts distribuidos saturen la BD)
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # Conexiones simultáneas mantenidas
    max_overflow=20,        # Conexiones extra permitidas en picos de tráfico
    pool_pre_ping=True      # Verifica si la conexión sigue viva antes de usarla
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener una sesión (Útil para FastAPI y Scripts)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()