from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .core.config import settings
from .db.sessions import shutdown_db_connections
from .routes import hero, skills, projects, contact, integrityBadge, tracks

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejador del ciclo de vida (Lifespan).
    Sustituye a los antiguos eventos startup/shutdown para una mejor 
    gestión de recursos asíncronos (TRD §5).
    """
    # Fase de Inicio: Aquí podrías inicializar pools o verificar conexiones
    yield
    # Fase de Cierre: Implementa el Graceful Shutdown (RF-6.4)
    await shutdown_db_connections()

# Inicialización de la App con Metadatos del PRD
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    # Documentación condicional para evitar "Security through obscurity" innecesario (TRD §5)
    openapi_url=settings.openapi_url,
    docs_url=f"{settings.API_V1_STR}/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url=None # ReDoc desactivado para minimizar ruido visual
)

# Configuración de CORS para el Frontend en Next.js 15+ (TRD §1)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "https://davidnava.vercel.app",
        "https://profesionalprofile.onrender.com/api/v1"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # Permite Content-Type, Authorization, etc.
)

# Registro de Rutas (Diseño basado en Dominios - TRD §2)
# Acto I: La Génesis
app.include_router(hero.router, prefix=settings.API_V1_STR)

# Acto II: Tríada del Conocimiento (Miller's Law)
app.include_router(skills.router, prefix=settings.API_V1_STR)

# Acto III: Evidencia Técnica (Glassmorphism & Stripe Demo)
app.include_router(projects.router, prefix=settings.API_V1_STR)

# Acto IV: Vínculo Humano & Gobernanza (Postel's Law)
app.include_router(contact.router, prefix=settings.API_V1_STR)
app.include_router(integrityBadge.router, prefix=settings.API_V1_STR)
app.include_router(tracks.router, prefix=settings.API_V1_STR)   

@app.get("/", tags=["Health"])
async def root():
    """Endpoint básico para validar que el viaje ha comenzado."""
    return {
        "status": "online",
        "journey": "The Tranquil Journey is running",
        "integrity": "verified"
    }