import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguegamefinder
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text, MetaData, Table
from database import engine

def sync_integral_nba_data():
    print("🚀 Iniciando descarga de LeagueGameFinder (Temporada 2025-26)...")
    
    # 1. Descarga de datos
    finder = leaguegamefinder.LeagueGameFinder(
        season_type_nullable="Regular Season",
        season_nullable="2025-26",
        league_id_nullable="00"
    )
    df_raw = finder.get_data_frames()[0]
    
    # Normalizamos nombres de columnas de la API (vienen en mayúsculas)
    df_raw.columns = [c.upper() for c in df_raw.columns]

    # 2. Consolidación para la tabla 'games'
    print("🛠️ Procesando lógica de partidos para la tabla 'games'...")
    games_consolidated = []
    
    for gid, group in df_raw.groupby('GAME_ID'):
        if len(group) < 2: continue 
        
        row_1 = group.iloc[0]
        row_2 = group.iloc[1]
        
        # Identificar Home/Away por el campo MATCHUP
        home_row = row_1 if 'vs.' in row_1['MATCHUP'] else row_2
        away_row = row_2 if 'vs.' in row_1['MATCHUP'] else row_1
        
        games_consolidated.append({
            'game_id': str(gid).zfill(10),
            'home_team_id': int(home_row['TEAM_ID']),
            'away_team_id': int(away_row['TEAM_ID']),
            'home_points': int(home_row['PTS']) if pd.notnull(home_row['PTS']) else 0,
            'away_points': int(away_row['PTS']) if pd.notnull(away_row['PTS']) else 0,
            'game_date': pd.to_datetime(home_row['GAME_DATE']).date(),
            'status': 'completed',
            'season_id': 22025
        })

    meta = MetaData()
    
    # 3. UPSERT EN 'games'
    if games_consolidated:
        print(f"📦 Sincronizando {len(games_consolidated)} partidos en 'games'...")
        table_games = Table('games', meta, autoload_with=engine)
        with engine.begin() as conn:
            stmt_g = insert(table_games).values(games_consolidated)
            stmt_g = stmt_g.on_conflict_do_update(
                index_elements=['game_id'],
                set_={
                    'home_points': stmt_g.excluded.home_points,
                    'away_points': stmt_g.excluded.away_points,
                    'status': stmt_g.excluded.status
                }
            )
            conn.execute(stmt_g)

    # 4. PREPARACIÓN PARA 'team_game_stats'
    print("📊 Procesando estadísticas por equipo...")
    
    # Mapeo exacto: API -> Tu Tabla PostgreSQL
    mapeo_stats = {
        'GAME_ID': 'game_id', 
        'TEAM_ID': 'team_id', 
        'PTS': 'pts',
        'FGM': 'fg_made', 
        'FGA': 'fg_attempted', 
        'FG_PCT': 'fg_percentage',
        'FG3M': 'three_p_made', 
        'FG3A': 'three_p_attempted', 
        'FG3_PCT': 'fg3_percentage',
        'FTM': 'ft_made', 
        'FTA': 'ft_attempted', 
        'FT_PCT': 'ft_percentage',
        'OREB': 'rebounds_offensive', 
        'DREB': 'rebounds_defensive',
        'REB': 'rebounds_total', 
        'AST': 'assists', 
        'STL': 'steals',
        'BLK': 'blocks', 
        'TOV': 'turnovers', 
        'PF': 'fouls',
        'MIN': 'minutes_played', 
        'WL': 'win'
    }

    # Seleccionamos solo las columnas necesarias y renombramos
    df_stats = df_raw[list(mapeo_stats.keys())].rename(columns=mapeo_stats).copy()
    
    # --- LIMPIEZA CRÍTICA DE DATOS ---
    df_stats['game_id'] = df_stats['game_id'].astype(str).str.zfill(10)
    df_stats['team_id'] = df_stats['team_id'].astype(int)
    
    # Manejo de la columna 'win'
    df_stats['win'] = df_stats['win'].map({'W': True, 'L': False}).fillna(False)
    
    # Convertir MIN a entero (a veces viene como "240" o "239:58")
    df_stats['minutes_played'] = pd.to_numeric(df_stats['minutes_played'], errors='coerce').fillna(240).astype(int)

    # Asegurar que todas las métricas numéricas NO sean NaN (aquí se soluciona lo de rebounds_defensive)
    cols_numericas = [
        'pts', 'fg_made', 'fg_attempted', 'three_p_made', 'three_p_attempted', 
        'ft_made', 'ft_attempted', 'rebounds_offensive', 'rebounds_defensive', 
        'rebounds_total', 'assists', 'steals', 'blocks', 'turnovers', 'fouls',
        'fg_percentage', 'fg3_percentage', 'ft_percentage'
    ]
    
    for col in cols_numericas:
        df_stats[col] = pd.to_numeric(df_stats[col], errors='coerce').fillna(0)
        # Si la columna es de conteo (no porcentaje), convertir a int
        if 'percentage' not in col:
            df_stats[col] = df_stats[col].astype(int)

    # 5. UPSERT EN 'team_game_stats'
    print(f"💾 Guardando estadísticas en 'team_game_stats'...")
    table_team_stats = Table('team_game_stats', meta, autoload_with=engine)
    
    with engine.begin() as conn:
        data_s = df_stats.to_dict(orient='records')
        stmt_s = insert(table_team_stats).values(data_s)
        
        # Identificamos las columnas a actualizar en caso de conflicto
        # Excluimos las llaves primarias/índices
        update_cols_s = {
            c.name: c for c in stmt_s.excluded 
            if c.name not in ['game_id', 'team_id']
        }
        
        conn.execute(stmt_s.on_conflict_do_update(
            index_elements=['game_id', 'team_id'], 
            set_=update_cols_s
        ))

    print("✅ Proceso completado exitosamente.")

if __name__ == "__main__":
    sync_integral_nba_data()