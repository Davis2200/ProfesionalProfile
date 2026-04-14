from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from database import engine 
from datetime import date

router = APIRouter()

@router.get("/calendar")
def get_calendar(target_date: date): # FastAPI validará que sea YYYY-MM-DD
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
        with engine.connect() as conn:
            result = conn.execute(query, {"d": target_date}).mappings().all()
            games = [dict(row) for row in result]

            # Mapeo de status
            status_map = {
                "completed": "completado",
                "in_progress": "en progreso",
                "scheduled": "agendado"
            }
            for game in games:
                game["status"] = status_map.get(game["status"], game["status"])

            return {"status": "success", "games": games}
    except Exception as e:
        print(f"Error en el Router: {e}")
        raise HTTPException(status_code=500, detail=str(e))