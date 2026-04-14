import pandas as pd
import time
import datetime
from datetime import date
from sqlalchemy import text
from nba_api.stats.endpoints import commonteamroster, commonplayerinfo
from database import engine 

def asegurar_jugadores_en_db(df_roster):
    if df_roster.empty: return
    
    ids_nba = [int(x) for x in df_roster['PLAYER_ID'].unique().tolist()]
    query = text("SELECT player_id FROM players WHERE player_id = ANY(:ids)")
    
    with engine.connect() as conn:
        existentes = pd.read_sql(query, conn, params={'ids': ids_nba})['player_id'].tolist()

    faltantes = list(set(ids_nba) - set(existentes))
    
    if faltantes:
        print(f"🔍 Registrando {len(faltantes)} jugadores nuevos...")
        for p_id in faltantes:
            try:
                p_info = commonplayerinfo.CommonPlayerInfo(player_id=p_id, timeout=15)
                p_df = p_info.get_data_frames()[0]
                full_name = p_df['DISPLAY_FIRST_LAST'].iloc[0]
                time.sleep(0.8) # Rate limit
            except Exception:
                full_name = f"Unknown Player {p_id}"

            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO players (player_id, name, is_active)
                    VALUES (:id, :name, :active)
                    ON CONFLICT (player_id) DO NOTHING
                """), {"id": p_id, "name": full_name, "active": True})

def procesar_rosters_completos():
    # Cambia esto a la fecha que necesites procesar (hoy o mañana)
    fecha_objetivo = datetime.date.today() + datetime.timedelta(days=1)
    
    query_games = text("""
        SELECT game_id, home_team_id, away_team_id, game_date 
        FROM games 
        WHERE game_date = :fecha
    """)
    
    with engine.connect() as conn:
        partidos = conn.execute(query_games, {"fecha": fecha_objetivo}).fetchall()

    if not partidos:
        print(f"📭 No hay partidos en games para {fecha_objetivo}")
        return

    for game_id, home_id, visitor_id, g_date in partidos:
        print(f"🏀 Juego {game_id}: {home_id} vs {visitor_id}")
        
        for team_id in [home_id, visitor_id]:
            try:
                # CommonTeamRoster trae a TODA la plantilla (Active + Bench)
                roster = commonteamroster.CommonTeamRoster(team_id=team_id, timeout=15)
                df_roster = roster.get_data_frames()[0]
                time.sleep(0.7)
            except Exception as e:
                print(f"⚠️ Error equipo {team_id}: {e}")
                continue

            if df_roster.empty: continue

            asegurar_jugadores_en_db(df_roster)

            data_to_insert = []
            for _, row in df_roster.iterrows():
                data_to_insert.append({
                    "g_id": game_id,
                    "p_id": row['PLAYER_ID'],
                    "t_id": team_id,
                    "starter": False, # Se actualiza después con el boxscore real
                    "avail": True,
                    "pos": row['POSITION'],
                    "g_date": g_date # ¡IMPORTANTE!
                })

            with engine.begin() as conn:
                upsert_query = text("""
                    INSERT INTO game_lineups (game_id, player_id, team_id, is_starter, is_available, position_d, game_date)
                    VALUES (:g_id, :p_id, :t_id, :starter, :avail, :pos, :g_date)
                    ON CONFLICT (game_id, player_id) 
                    DO UPDATE SET 
                        position_d = EXCLUDED.position_d,
                        game_date = EXCLUDED.game_date;
                """)
                conn.execute(upsert_query, data_to_insert)
            
            print(f"   ✅ {len(data_to_insert)} jugadores (total equipo) listos para {team_id}")

if __name__ == "__main__":
    procesar_rosters_completos()