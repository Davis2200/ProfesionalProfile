from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()

@router.get("/highlights")
def get_player_highlights(search: str = None):
    # Temporada actual constante
    CURRENT_SEASON = 22025
    search_filter = f"AND p.name ILIKE '%{search}%'" if search else ""
    
    query = text(f"""
        SELECT 
            p.player_id, 
            p.name,
            CAST(COALESCE(pt.avg_points, 0) AS FLOAT) as avg_p,
            CAST(COALESCE(pt.med_points, 0) AS FLOAT) as med_p,
            CAST(COALESCE(pt.std_points, 0) AS FLOAT) as std_p,
            COALESCE(pt.has_double_double, FALSE) as dd,
            COALESCE(pt.mode_points, 0) as mode_pts,
            COALESCE(pt.has_triple_double, FALSE) as td,
            
            -- Ahora sí usamos game_date para traer los puntos reales del último encuentro
            COALESCE((
                SELECT ps.points 
                FROM public.players_stats ps
                WHERE ps.player_id = p.player_id 
                  AND ps.season_id = :season
                ORDER BY ps.game_date DESC, ps.performance_id DESC 
                LIMIT 1
            ), 0) as last_pts,
            
            -- Predicción más reciente de StatsBet
            COALESCE((
                SELECT pp.predicted_points 
                FROM public.player_predictions pp
                WHERE pp.player_id = p.player_id 
                ORDER BY pp.prediction_date DESC LIMIT 1
            ), 0.0) as pred_pts
            
        FROM public.players p
        LEFT JOIN public.player_trends pt ON p.player_id = pt.player_id
        WHERE 1=1
        {search_filter}
        ORDER BY pt.avg_points DESC NULLS LAST
        LIMIT 10
    """)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"season": CURRENT_SEASON}).mappings().all()
            
            output = []
            for r in result:
                # Solo incluimos jugadores que tengan al menos un juego en la temporada
                if r["last_pts"] is not None:
                    output.append({
                        "id": r["player_id"],
                        "name": r["name"],
                        "last_game_points": int(r["last_pts"]),
                        "stats": {
                            "Promedio": round(float(r["avg_p"]), 1),
                            "Mediana": round(float(r["med_p"]), 1),
                            "Moda": int(r["mode_pts"]),
                            "Desviación": round(float(r["std_p"]), 1)
                        },
                        "is_dd": r["dd"],
                        "is_td": r["td"],
                        "prediction": round(float(r["pred_pts"]), 1)
                    })
            
            return {
                "top_scorers": output,
                "double_doubles": [p for p in output if p["is_dd"]],
                "triple_doubles": [p for p in output if p["is_td"]]
            }
    except Exception as e:
        print(f"❌ Error en SQL: {e}")
        return {"top_scorers": [], "double_doubles": [], "triple_doubles": []}
    
@router.get("/double-impact")
def get_double_double_masters(search: str = None):
    CURRENT_SEASON = 22025 
    search_term = f"%{search}%" if search else "%"
    
    query = text("""
        SELECT 
            p.player_id, p.name,
            CAST(pt.avg_points AS FLOAT) as avg_p,
            pt.mode_points as mode_p,
            pt.med_points as med_p,
            pt.std_points as std_p,
            (SELECT json_build_object(
                'PTS', ps.points, 
                'REB', ps.rebounds_total, 
                'AST', ps.assists,
                'STL', ps.steals,
                'BLK', ps.blocks
             )
             FROM public.players_stats ps
             WHERE ps.player_id = p.player_id AND ps.season_id = :season
             ORDER BY ps.game_date DESC, ps.performance_id DESC 
             LIMIT 1) as last_game
        FROM public.players p
        JOIN public.player_trends pt ON p.player_id = pt.player_id
        WHERE pt.has_double_double = TRUE AND p.name ILIKE :search
        ORDER BY (pt.avg_points + pt.avg_rebounds + pt.avg_assists) DESC
        LIMIT 20
    """)

    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"search": search_term, "season": CURRENT_SEASON}).mappings().all()
            output = []
            for r in result:
                lg = r["last_game"] or {}
                achievements = [f"{val} {key}" for key, val in lg.items() if val >= 10]
                
                output.append({
                    "id": r["player_id"],
                    "name": r["name"],
                    "stats": {
                        "Promedio": round(r["avg_p"], 1),
                        "Mediana": round(r["med_p"] or r["avg_p"], 1),
                        "Moda": r["mode_p"] or 0,
                        "Desviación": round(r["std_p"] or 0, 1)
                    },
                    "last_game_points": " | ".join(achievements) if achievements else "0 PTS",
                    "prediction": 0.0
                })
            return {"double_doubles": output}
    except Exception as e:
        return {"error": str(e), "double_doubles": []}

@router.get("/triple-threat")
def get_triple_double_elite(search: str = None):
    CURRENT_SEASON = 22025
    search_term = f"%{search}%" if search else "%"
    
    query = text("""
        SELECT 
            p.player_id, p.name,
            CAST(pt.avg_points AS FLOAT) as avg_p,
            pt.mode_points as mode_p,
            pt.med_points as med_p,
            pt.std_points as std_p,
            (SELECT json_build_object(
                'PTS', ps.points, 'REB', ps.rebounds_total, 
                'AST', ps.assists, 'STL', ps.steals, 'BLK', ps.blocks
             )
             FROM public.players_stats ps
             WHERE ps.player_id = p.player_id AND ps.season_id = :season
             ORDER BY ps.game_date DESC LIMIT 1) as last_game
        FROM public.players p
        JOIN public.player_trends pt ON p.player_id = pt.player_id
        WHERE pt.has_triple_double = TRUE AND p.name ILIKE :search
        ORDER BY (pt.avg_points + pt.avg_rebounds + pt.avg_assists) DESC
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"search": search_term, "season": CURRENT_SEASON}).mappings().all()
            output = []
            for r in result:
                lg = r["last_game"] or {}
                achievements = [f"{val} {key}" for key, val in lg.items() if val >= 10]
                
                output.append({
                    "id": r["player_id"],
                    "name": r["name"],
                    "stats": {
                        "Promedio": round(r["avg_p"], 1),
                        "Mediana": round(r["med_p"] or r["avg_p"], 1),
                        "Moda": r["mode_p"] or 0,
                        "Desviación": round(r["std_p"] or 0, 1)
                    },
                    "last_game_points": " | ".join(achievements) if achievements else "STATS INCOMPLETAS",
                    "prediction": 0.0
                })
            return {"triple_doubles": output}
    except Exception as e:
        return {"error": str(e), "triple_doubles": []}    
    
    

@router.get("/scout")
def universal_player_scout(name: str):
    """Búsqueda rápida de cualquier jugador con sus tendencias actuales"""
    query = text("""
        SELECT p.name, pt.avg_points, pt.mode_points, pt.has_double_double as dd, pt.has_triple_double as td
        FROM public.players p
        LEFT JOIN public.player_trends pt ON p.player_id = pt.player_id
        WHERE p.name ILIKE :name
        LIMIT 5
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"name": f"%{name}%"}).mappings().all()
            return {"results": [dict(r) for r in result]}
    except Exception as e:
        return {"error": str(e)}
