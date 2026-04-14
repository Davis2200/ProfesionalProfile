import os
import socket  # Importante para resolver el nombre
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# --- LÓGICA DE RESOLUCIÓN DE IP ---
def resolve_host(host):
    try:
        # Intenta convertir el nombre de host (ej: 'debian.local') en una IP
        return socket.gethostbyname(host)
    except socket.gaierror:
        # Si falla (porque ya es una IP o el host no existe), devuelve el original
        return host

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# Obtenemos el host del .env y lo resolvemos dinámicamente
raw_host = os.getenv("DB_HOST")
DB_HOST = resolve_host(raw_host) 

DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construir la URL de conexión
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# El Engine con Pool de conexiones
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()