from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.calendar import router as calendar_router
from api.routes.jugadores import router as players_router

app = FastAPI(title="StatsBet API - Local")

# Configuración de CORS para acceso local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# ...
app.include_router(players_router, prefix="/players")
# Incluimos las rutas de lógica
app.include_router(calendar_router, prefix="/predictions")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)