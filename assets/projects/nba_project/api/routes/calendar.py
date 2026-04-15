import sys
import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date

# --- AJUSTE DE IMPORTACIÓN ---
# Permitir que el router encuentre 'database.py' en la raíz
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Importamos la dependencia get_db (en lugar del engine directo)
try:
    from database import get_db
except ImportError:
    print("❌ Error: No se pudo importar get_db desde database.py")
    raise

router = APIRouter()

@router.get("/calendar")
def get_calendar(target_date: date, db: Session = Depends(get_db)):
    """
    Obtiene el calendario de juegos de la NBA para una fecha específica.
    """
    query = text("""
        SELECT 
            g.game_id as id, t1.name as local, t1.team_id as h_id,
            t2.name as visitante, t2.team_id as v_id,
            g.status, COALESCE(s.arena_name, 'NBA Arena') as estadio,
            TO_CHAR(g.scheduled_date_mx, 'HH24:MI') as hora,
            TO_CHAR(g.game_date, 'TMDY DD/MM') as f_corta,
            COALESCE(g.home_points, 0) as pts_l,
            COALESCE(g.away_points, 0) as pts_v
        FROM games g
        JOIN teams t1 ON g.home_team_id = t1.team_id
        JOIN teams t2 ON g.away_team_id = t2.team_id
        LEFT JOIN stadiums s ON t1.team_id = s.team_id
        WHERE g.game_date = :d 
        ORDER BY g.scheduled_date_mx ASC
    """)
    
    try:
        # Usamos la sesión 'db' inyectada por FastAPI
        result = db.execute(query, {"d": target_date}).mappings().all()
        games = [dict(row) for row in result]

        # Mapeo de status para el dashboard
        status_map = {
            "completed": "completado",
            "in_progress": "en progreso",
            "scheduled": "agendado",
            "Final": "completado" # Agregado por si la API de NBA usa 'Final'
        }
        
        for game in games:
            game["status"] = status_map.get(game["status"], game["status"])

        return {
            "status": "success", 
            "date": target_date,
            "count": len(games),
            "games": games
        }
        
    except Exception as e:
        print(f"🔴 Error en el Router de Calendario: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error consultando la base de datos en DavisNA: {str(e)}"
        )