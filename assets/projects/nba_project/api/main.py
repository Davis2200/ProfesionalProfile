from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importamos las rutas y la base de datos
from database import engine, Base
from api.routes.calendar import router as calendar_router
from api.routes.jugadores import router as players_router

# Crear las tablas si no existen (opcional, pero útil)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="StatsBet API - Conectada a DavisNA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(players_router, prefix="/players", tags=["Jugadores"])
app.include_router(calendar_router, prefix="/predictions", tags=["Predicciones"])

@app.get("/check_connection")
def check_connection():
    from database import DB_HOST
    return {
        "status": "Ready",
        "resolved_ip": DB_HOST,
        "target_machine": "DavisNA"
    }

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 permite que Streamlit (u otros) lleguen a la API
    uvicorn.run(app, host="0.0.0.0", port=8000)