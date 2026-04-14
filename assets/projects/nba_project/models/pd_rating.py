import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguegamelog
from sqlalchemy import text
from database import engine

def sync_team_defense_metrics(season='2025-26'):
    print(f"🚀 Calculando Defensive Rating y Pace para {season}...")
    
    logs = leaguegamelog.LeagueGameLog(season=season, player_or_team_abbreviation='T').get_data_frames()[0]
    
    valid_prefixes = ('002', '004', '005')
    logs = logs[logs['GAME_ID'].str.startswith(valid_prefixes)].copy()
    logs['GAME_DATE'] = pd.to_datetime(logs['GAME_DATE'])

    # Cruzamos el juego con el oponente para ver cuánto le anotaron
    opps = logs[['GAME_ID', 'TEAM_ID', 'PTS', 'FGA', 'FTA', 'OREB', 'TOV']].copy()
    df = logs.merge(opps, on='GAME_ID', suffixes=('', '_OPP'))
    df = df[df['TEAM_ID'] != df['TEAM_ID_OPP']] # Filtrar para que quede Equipo vs Rival

    # Estimación de Posesiones (Fórmula Hollinger simplificada)
    df['possessions'] = 0.5 * (
        (df['FGA'] + 0.44 * df['FTA'] - df['OREB'] + df['TOV']) +
        (df['FGA_OPP'] + 0.44 * df['FTA_OPP'] - df['OREB_OPP'] + df['TOV_OPP'])
    )
    
    # Defensive Rating: Puntos permitidos por cada 100 posesiones
    df['def_rating'] = (df['PTS_OPP'] / df['possessions'].replace(0, 1)) * 100

    # Promedios móviles L5 (Tendencia reciente)
    df = df.sort_values(['TEAM_ID', 'GAME_DATE'])
    df['pa5'] = df.groupby('TEAM_ID')['PTS_OPP'].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df['pc5'] = df.groupby('TEAM_ID')['possessions'].transform(lambda x: x.rolling(5, min_periods=1).mean())

    data_to_save = []
    for _, row in df.iterrows():
        data_to_save.append({
            'tid': int(row['TEAM_ID']),
            'gid': str(row['GAME_ID']),
            'gdt': row['GAME_DATE'],
            'dr': float(row['def_rating']),
            'pa5': float(row['pa5']),
            'pc5': float(row['pc5'])
        })

    with engine.begin() as conn:
        print(f"📥 Sincronizando {len(data_to_save)} registros de defensa...")
        conn.execute(text("""
            INSERT INTO team_defense_history (team_id, game_id, game_date, def_rating, pts_allowed_l5, pace_l5)
            VALUES (:tid, :gid, :gdt, :dr, :pa5, :pc5)
            ON CONFLICT (team_id, game_id) DO UPDATE SET
                def_rating = EXCLUDED.def_rating,
                pts_allowed_l5 = EXCLUDED.pts_allowed_l5,
                pace_l5 = EXCLUDED.pace_l5;
        """), data_to_save)
    print("✅ pd_rating completado.")

if __name__ == "__main__":
    sync_team_defense_metrics()