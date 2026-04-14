import pandas as pd
import time
from datetime import datetime, timedelta
from nba_api.stats.endpoints import scoreboardv3
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import MetaData, Table
from database import engine

def normalize_status(raw_status: str) -> str:
    if not raw_status:
        return "scheduled"

    s = raw_status.strip().lower()

    # Juegos en progreso
    if any(keyword in s for keyword in ["qtr", "half", "in progress"]):
        return "in_progress"

    # Juegos finalizados
    if "final" in s:
        return "completed"

    # Juegos agendados (horarios tipo "7:30 pm et")
    if "pm et" in s or "am et" in s or "scheduled" in s:
        return "scheduled"

    # Default
    return "scheduled"

def scheduler_future_games(days_to_fetch=15):
    print(f"📅 StatsBet: Iniciando sincronización de {days_to_fetch} días (Extracción JSON)...")
    
    all_games = []
    start_date = datetime.now()

    for i in range(days_to_fetch):
        current_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        print(f"🔍 Procesando fecha: {current_date}...", end="\r")
        
        try:
            sb = scoreboardv3.ScoreboardV3(game_date=current_date)
            data_json = sb.get_dict()
            games_list = data_json.get('scoreboard', {}).get('games', [])

            if games_list:
                for game in games_list:
                    game_id = str(game.get('gameId')).zfill(10)

                    # ✅ Hora oficial del endpoint
                    game_time_utc = game.get("gameTimeUTC")
                    dt_us = pd.Timestamp(game_time_utc).tz_convert("US/Eastern").tz_localize(None)
                    dt_mx = pd.Timestamp(game_time_utc).tz_convert("America/Mexico_City").tz_localize(None)

                    # ✅ Season ID directo del JSON
                    season_id = str(game.get("seasonId", "22025"))

                    # ✅ Normalización del status
                    status = normalize_status(game.get("gameStatusText", ""))

                    all_games.append({
                        'game_id': game_id,
                        'season_id': season_id,
                        'game_date': current_date,
                        'home_team_id': game.get('homeTeam', {}).get('teamId'),
                        'away_team_id': game.get('awayTeam', {}).get('teamId'),
                        'status': status,
                        'scheduled_date_us': dt_us,
                        'scheduled_date_mx': dt_mx
                    })
            
            time.sleep(0.7) 
            
        except Exception as e:
            print(f"\n⚠️ Error extrayendo JSON en {current_date}: {e}")

    if not all_games:
        print("\n❌ No se encontraron juegos.")
        return

    df_final = pd.DataFrame(all_games)
    df_final = df_final.dropna(subset=['game_id', 'home_team_id', 'away_team_id'])

    try:
        metadata = MetaData()
        table = Table('games', metadata, autoload_with=engine)
        
        records = df_final.to_dict(orient='records')
        
        stmt = insert(table).values(records)
        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=['game_id'],
            set_={
                'status': stmt.excluded.status,
                'game_date': stmt.excluded.game_date,
                'scheduled_date_mx': stmt.excluded.scheduled_date_mx,
                'scheduled_date_us': stmt.excluded.scheduled_date_us,
                'home_team_id': stmt.excluded.home_team_id,
                'away_team_id': stmt.excluded.away_team_id,
                'season_id': stmt.excluded.season_id
            }
        )

        with engine.begin() as conn:
            conn.execute(upsert_stmt)
            
        print(f"\n🚀 ¡Éxito! {len(df_final)} juegos insertados/actualizados.")
        
    except Exception as e:
        print(f"\n❌ Error en la carga a base de datos: {e}")

if __name__ == "__main__":
    scheduler_future_games(15)
