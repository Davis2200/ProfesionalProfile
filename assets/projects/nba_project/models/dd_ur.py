import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguegamelog
from sqlalchemy import text
from database import engine

def sync_advanced_player_metrics(season='2025-26'):
    print(f"🚀 Calculando Usage Rate y Descanso para {season}...")
    
    # 1. Descarga de datos
    p_logs = leaguegamelog.LeagueGameLog(season=season, player_or_team_abbreviation='P').get_data_frames()[0]
    t_logs = leaguegamelog.LeagueGameLog(season=season, player_or_team_abbreviation='T').get_data_frames()[0]

    # Filtro de ligas (Regular=002, Playoffs=004, Play-in=005)
    valid_prefixes = ('002', '004', '005')
    p_logs = p_logs[p_logs['GAME_ID'].str.startswith(valid_prefixes)].copy()
    t_logs = t_logs[t_logs['GAME_ID'].str.startswith(valid_prefixes)].copy()

    # Preparar totales de equipo para el Usage Rate
    t_totals = t_logs[['GAME_ID', 'TEAM_ID', 'FGA', 'FTA', 'TOV']].rename(
        columns={'FGA': 'T_FGA', 'FTA': 'T_FTA', 'TOV': 'T_TOV'}
    )
    
    # Merge de jugador con su equipo en ese juego
    df = p_logs.merge(t_totals, on=['GAME_ID', 'TEAM_ID'])
    
    # Cálculo de Usage Rate (Fórmula NBA estándar simplificada)
    df['usage_rate'] = 100 * (
        (df['FGA'] + 0.44 * df['FTA'] + df['TOV']) / 
        (df['T_FGA'] + 0.44 * df['T_FTA'] + df['T_TOV']).replace(0, 1)
    )

    # Cálculo de Días de Descanso (Usando GAME_DATE en mayúsculas como viene de la API)
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    df = df.sort_values(['PLAYER_ID', 'GAME_DATE'])
    df['prev_date'] = df.groupby('PLAYER_ID')['GAME_DATE'].shift(1)
    df['rest_days'] = (df['GAME_DATE'] - df['prev_date']).dt.days.fillna(4)
    df['rest_days'] = df['rest_days'].clip(0, 4).astype(int)

    data_to_save = []
    for _, row in df.iterrows():
        data_to_save.append({
            'pid': int(row['PLAYER_ID']),
            'gid': str(row['GAME_ID']),
            'tid': int(row['TEAM_ID']),
            'ur': float(row['usage_rate']),
            'rd': int(row['rest_days'])
        })

    with engine.begin() as conn:
        print(f"📥 Upserting {len(data_to_save)} registros en player_advanced_metrics...")
        conn.execute(text("""
            INSERT INTO player_advanced_metrics (player_id, game_id, team_id, usage_rate, rest_days)
            VALUES (:pid, :gid, :tid, :ur, :rd)
            ON CONFLICT (player_id, game_id) DO UPDATE SET
                usage_rate = EXCLUDED.usage_rate,
                rest_days = EXCLUDED.rest_days;
        """), data_to_save)
    print("✅ dd_ur completado.")

if __name__ == "__main__":
    sync_advanced_player_metrics()