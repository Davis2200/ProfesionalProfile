import pandas as pd
import requests
import time
from datetime import datetime
from sqlalchemy import MetaData, Table, select, and_, or_
from sqlalchemy.dialects.postgresql import insert
from database import engine 

def get_games_to_update():
    """Trae los Game IDs de fechas específicas que no están completados."""
    metadata = MetaData()
    table = Table('games', metadata, autoload_with=engine)
    
    target_dates = ['2026-04-12']
    #target_dates = [datetime.now().date().strftime('%Y-%m-%d')]
    # -------------------------------

    # Filtro: Que la fecha esté en nuestra lista Y el status NO sea 'completed'
    query = select(table.c.game_id).where(
        and_(
            table.c.game_date.in_(target_dates)
        )
    )
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            # Mantenemos el ID como string con ceros a la izquierda (10 dígitos)
            return [str(row[0]).zfill(10) for row in result]
    except Exception as e:
        print(f"❌ Error al consultar la base de datos: {e}")
        return []

def apply_update(game_dict):
    """Realiza el UPSERT para actualizar solo el score y el status."""
    metadata = MetaData()
    table = Table('games', metadata, autoload_with=engine)
    
    stmt = insert(table).values(game_dict)
    
    # Solo actualizamos los campos que cambian al terminar el juego
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=['game_id'],
        set_={
            'status': stmt.excluded.status,
            'home_points': stmt.excluded.home_points,
            'away_points': stmt.excluded.away_points,
            'game_clock': stmt.excluded.game_clock,
            'game_period': stmt.excluded.game_period
        }
    )
    
    with engine.begin() as conn:
        conn.execute(upsert_stmt)

def repair_scores_pipeline():
    game_ids = get_games_to_update()
    
    if not game_ids:
        print("🙌 Todo está al día. No hay juegos pendientes de score en esas fechas.")
        return

    print(f"🔧 Se encontraron {len(game_ids)} juegos para actualizar marcadores...")

    for gid in game_ids:
        # Usamos el CDN de LiveData, es el más rápido para resultados finales
        url = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{gid}.json"
        
        try:
            print(f"🧐 Consultando API para GameID: {gid}...", end=" ")
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"⚠️ Salto: No hay datos aún (Status {response.status_code})")
                continue
            
            game_data = response.json()['game']
            status_text = game_data['gameStatusText']
            
            # Solo actualizamos si el juego realmente terminó según la NBA
            if 'Final' in status_text:
                update_payload = {
                    'game_id': gid, # Mantenemos el string para no romper ceros
                    'status': 'completed',
                    'home_points': game_data['homeTeam']['score'],
                    'away_points': game_data['awayTeam']['score'],
                    'game_clock': '00:00',
                    'game_period': 'Final'
                }
                
                apply_update(update_payload)
                h_score = game_data['homeTeam']['score']
                a_score = game_data['awayTeam']['score']
                print(f"✅ ¡Marcador actualizado! ({a_score} - {h_score})")
            else:
                print(f"⏳ El juego aún no termina (Status: {status_text})")

            # Respeto al Rate Limit de la NBA
            time.sleep(0.5) 

        except Exception as e:
            print(f"❌ Error crítico en {gid}: {e}")

if __name__ == "__main__":
    repair_scores_pipeline()