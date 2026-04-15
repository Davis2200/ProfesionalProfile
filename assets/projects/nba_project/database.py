import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

def resolve_db_host(host_name):
    """
    Intenta resolver el nombre de la PC (ej. DavisNA) a su IP local.
    Si falla, devuelve localhost por seguridad.
    """
    try:
        # Esto resolverá 'DavisNA' a algo como '192.168.1.X'
        return socket.gethostbyname(host_name)
    except socket.gaierror:
        print(f"⚠️ No se pudo resolver el host {host_name}. Usando 127.0.0.1")
        return "127.0.0.1"

# --- CONFIGURACIÓN ---
# Usamos 'DavisNA' como valor por defecto si no está en el .env
RAW_HOST = os.getenv("DB_HOST", "DavisNA")
DB_HOST = resolve_db_host(RAW_HOST)

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "nba_stats")

# URL de conexión para PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuración del motor
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Verifica que la conexión esté viva antes de usarla
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()