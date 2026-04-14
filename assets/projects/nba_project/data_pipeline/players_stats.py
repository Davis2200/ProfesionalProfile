import pandas as pd
import time
from datetime import datetime, timedelta
from sqlalchemy import text, inspect
from nba_api.stats.endpoints import boxscoretraditionalv3, commonplayerinfo
from database import engine 

# --- FUNCIONES DE UTILIDAD ---

def clean_minutes(min_str):
    """Convierte 'MM:SS' a float (ej: '24:30' -> 24.5)"""
    if pd.isna(min_str) or min_str == "":
        return 0.0
    try:
        min_str = str(min_str)
        if ':' in min_str:
            m, s = map(int, min_str.split(':'))
            return round(m + (s / 60), 2)
        return float(min_str)
    except:
        return 0.0

def obtener_columnas_db(table_name):
    """Consulta dinámicamente las columnas de la tabla en PostgreSQL."""
    inspector = inspect(engine)
    return [col['name'] for col in inspector.get_columns(table_name)]

# --- LÓGICA DE EXTRACCIÓN Y PROCESAMIENTO ---

def fetch_and_process_boxscores(season_id=22025, days_back=1):
    """
    Busca juegos activos o terminados y descarga sus estadísticas.
    Actualiza registros incluso si ya existen (para juegos en curso).
    """
    date_limit = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    print(f"📅 StatsBet: Sincronizando juegos desde {date_limit}...")

    # MODIFICACIÓN: Eliminamos el filtro de "p.game_id IS NULL" para permitir 
    # actualizar juegos que ya tienen algunos registros pero no están completos.
    query = text("""
        SELECT DISTINCT g.game_id, g.status
        FROM games g
        WHERE g.season_id = :sid
          AND g.game_date >= :date_limit
          AND g.status IN ('completed', 'in_progress', 'Live')
    """)

    with engine.connect() as conn:
        consulta = pd.read_sql(query, conn, params={
            "sid": str(season_id),
            "date_limit": date_limit
        })

    game_ids = consulta['game_id'].tolist()
    if not game_ids:
        print("☕ No hay juegos nuevos o activos para procesar.")
        return None

    print(f"🏀 Procesando {len(game_ids)} juegos (Activos/Terminados).")

    box_score_up = []
    for gid in game_ids:
        str_gid = str(gid).zfill(10)
        try:
            print(f"   📥 Descargando Stats de Juego: {str_gid}...")
            box = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=str_gid, timeout=6)
            df = box.get_data_frames()[0]

            if not df.empty:
                df.columns = [c.lower() for c in df.columns]
                box_score_up.append(df)
            
            time.sleep(1.0) # Respetar rate limit de NBA API
        except Exception as e:
            print(f"   ⚠️ Error en juego {str_gid}: {e}")
            time.sleep(2)

    if not box_score_up:
        return None

    df_final = pd.concat(box_score_up, ignore_index=True)

    # MAPEO DE COLUMNAS V3 -> DB (Ajustado a tu esquema)
    mapeo = {
        'gameid': 'game_id', 
        'personid': 'player_id', 
        'teamid': 'team_id',
        'points': 'points', 
        'assists': 'assists', 
        'reboundstotal': 'rebounds',
        'steals': 'steals', 
        'blocks': 'blocks', 
        'turnovers': 'turnovers',
        'minutes': 'minutes_played', 
        'threepointersmade': 'three_p_made',
        'threepointersattempted': 'three_p_attempted', 
        'threepointerspercentage': 'three_p_percentage',
        'reboundsoffensive': 'rebounds_offensive', 
        'reboundsdefensive': 'rebounds_defensive',
        'plusminuspoints': 'plus_minus', 
        'freethrowsmade': 'free_throws_made',
        'freethrowsattempted': 'free_throws_attempted', 
        'freethrowspercentage': 'free_throws_percentage',
        'fieldgoalsmade': 'field_goal_made', 
        'fieldgoalsattempted': 'field_goal_attempted',
        'fieldgoalspercentage': 'field_goal_percentage', 
        'foulspersonal': 'personal_fouls'
    }

    df_final = df_final.rename(columns=mapeo)

    # Limpieza de datos
    df_final['minutes_played'] = df_final['minutes_played'].apply(clean_minutes)
    df_final = df_final.fillna(0)
    df_final['season_id'] = season_id
    df_final['game_id'] = df_final['game_id'].astype(str).str.zfill(10)
    
    # Filtrar solo columnas existentes en DB
    db_columns = obtener_columnas_db('players_stats')
    df_final = df_final[[c for c in df_final.columns if c in db_columns]].copy()

    return df_final

# --- GESTIÓN DE INTEGRIDAD ---

def asegurar_jugadores_en_db(df_stats):
    """Registra jugadores nuevos si no existen en la tabla 'players'."""
    if df_stats.empty: return
    
    ids_nba = [int(x) for x in df_stats['player_id'].unique().tolist()]
    query = text("SELECT player_id FROM players WHERE player_id = ANY(:ids)")
    
    with engine.connect() as conn:
        existentes = pd.read_sql(query, conn, params={'ids': ids_nba})['player_id'].tolist()

    faltantes = list(set(ids_nba) - set(existentes))
    
    if faltantes:
        print(f"👤 Registrando {len(faltantes)} jugadores nuevos...")
        for p_id in faltantes:
            try:
                p_info = commonplayerinfo.CommonPlayerInfo(player_id=p_id, timeout=10)
                p_df = p_info.get_data_frames()[0]
                full_name = p_df['DISPLAY_FIRST_LAST'].iloc[0]
            except:
                full_name = f"Unknown Player {p_id}"

            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO players (player_id, name, is_active)
                    VALUES (:id, :name, :active)
                    ON CONFLICT (player_id) DO NOTHING
                """), {"id": p_id, "name": full_name, "active": True})
            time.sleep(0.6)

# --- CARGA MASIVA (UPSERT) ---

def ejecutar_upsert_stats(df, table_name):
    """
    Inserta o actualiza estadísticas. 
    Crucial para completar datos de juegos que iniciaron pero no terminaron.
    """
    temp_table = f"temp_sync_stats"
    
    cols_all = [f'"{c}"' for c in df.columns]
    # Columnas a actualizar si hay conflicto (todas menos las llaves primarias)
    cols_update = [f'"{c}" = EXCLUDED."{c}"' for c in df.columns if c not in ['game_id', 'player_id']]

    try:
        with engine.begin() as conn:
            # Subida rápida a tabla temporal
            df.to_sql(temp_table, conn, index=False, if_exists='replace')
            
            # Query de Upsert
            sql = f"""
                INSERT INTO {table_name} ({", ".join(cols_all)})
                SELECT {", ".join(cols_all)} FROM {temp_table}
                ON CONFLICT (game_id, player_id)
                DO UPDATE SET {", ".join(cols_update)};
            """
            conn.execute(text(sql))
            conn.execute(text(f"DROP TABLE IF EXISTS {temp_table}"))
        print(f"✅ Sincronización exitosa: {len(df)} registros procesados.")
    except Exception as e:
        print(f"❌ Error en Upsert: {e}")

# --- FLUJO PRINCIPAL ---

if __name__ == "__main__":
    # season_id 22025 para esta temporada. 
    # days_back=2 es ideal para asegurar que no falte nada del fin de semana.
    df_stats = fetch_and_process_boxscores(season_id=22025, days_back=1)

    if df_stats is not None and not df_stats.empty:
        asegurar_jugadores_en_db(df_stats)
        
        print(f"🚀 Iniciando actualización en base de datos...")
        ejecutar_upsert_stats(df_stats, 'players_stats')
        print("✨ Proceso terminado.")
    else:
        print("☕ Sin datos nuevos para procesar.")