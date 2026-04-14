import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from nba_api.live.nba.endpoints import scoreboard
from database import engine 

def points_live():
    board = scoreboard.ScoreBoard()
    games_live = board.games.get_dict()
    data_list = []
    
    for game in games_live:
        # Mantenemos el game_id como string y aseguramos los 10 dígitos
        str_gid = str(game['gameId']).zfill(10)
        
        data_list.append({
            'game_id': str_gid,
            'status': game['gameStatusText'],
            'home_points': game['homeTeam']['score'],
            'away_points': game['awayTeam']['score']
        })
    
    df = pd.DataFrame(data_list)
    
    if not df.empty:
        # Lógica de unificación de estados mejorada para evitar falsos 'in_progress'
        def unificar_estado(text):
            text_lower = text.lower()
            if 'final' in text_lower:
                return 'completed'
            if any(q in text_lower for q in ['q1', 'q2', 'q3', 'q4', 'ot', 'half', 'end', 'qtr']):
                return 'in_progress'
            if any(t in text_lower for t in ['am', 'pm', 'et']):
                return 'scheduled'
            return 'in_progress'

        df['status'] = df['status'].apply(unificar_estado)
        
        # ELIMINADO: df['game_id'].astype(int) 
        # Ahora se queda como objeto/string de pandas
        
    return df

def update_scores(df):
    """Realiza el UPDATE basado en el ID (String/Varchar)"""
    if df.empty:
        print("☕ No hay juegos en la cartelera de hoy.")
        return

    metadata = MetaData()
    # Cargamos la tabla 'games' desde la DB
    table = Table('games', metadata, autoload_with=engine)
    
    # Convertir a lista de diccionarios
    data = df.to_dict(orient='records')
    
    # Preparar el Upsert de PostgreSQL
    stmt = insert(table).values(data)
    
    # Definimos qué columnas se sobreescriben al detectar el mismo game_id
    update_cols = {
        'status': stmt.excluded.status,
        'home_points': stmt.excluded.home_points,
        'away_points': stmt.excluded.away_points
    }
    
    # Ejecutar ON CONFLICT sobre game_id (ahora comparando strings)
    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=['game_id'], 
        set_=update_cols
    )

    try:
        with engine.begin() as conn:
            conn.execute(upsert_stmt)
            print(f"✅ LiveScores: {len(df)} partidos actualizados en la DB.")
    except Exception as e:
        print(f"❌ Error al actualizar LiveScores: {e}")
        
if __name__ == "__main__":
    # Ejecución manual de prueba
    df_updates = points_live()
    update_scores(df_updates)
    
    if not df_updates.empty:
        print("\n--- Vista previa de los datos enviados ---")
        print(df_updates[['game_id', 'status', 'home_points', 'away_points']].head())