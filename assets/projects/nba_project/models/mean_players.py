import pandas as pd
import numpy as np
from nba_api.stats.endpoints import playergamelogs
from sqlalchemy import text
from database import engine

def clean_data(d):
    clean_dict = {}
    for key, value in d.items():
        if isinstance(value, (np.float64, np.float32)):
            val = float(value)
        elif isinstance(value, (np.int64, np.int32)):
            val = int(value)
        elif isinstance(value, np.bool_):
            val = bool(value)
        else:
            val = value
        if isinstance(val, float) and np.isnan(val):
            val = None
        clean_dict[key] = val
    return clean_dict

def ensure_players_exist(conn, logs_df):
    unique_players = logs_df[['PLAYER_ID', 'PLAYER_NAME']].drop_duplicates()
    existing_ids = pd.read_sql("SELECT player_id FROM players", engine)['player_id'].tolist()
    missing_players = unique_players[~unique_players['PLAYER_ID'].isin(existing_ids)]
    
    for _, row in missing_players.iterrows():
        p_name = row['PLAYER_NAME'] or f"Unknown Player ({row['PLAYER_ID']})"
        conn.execute(text("""
            INSERT INTO players (player_id, name, is_active)
            VALUES (:pid, :pname, True) ON CONFLICT (player_id) DO NOTHING
        """), {"pid": int(row['PLAYER_ID']), "pname": p_name})

def ensure_games_exist(conn, logs_df):
    unique_games = logs_df[['GAME_ID', 'GAME_DATE', 'SEASON_YEAR']].drop_duplicates()
    existing_gids = pd.read_sql("SELECT game_id FROM games", engine)['game_id'].tolist()
    missing_games = unique_games[~unique_games['GAME_ID'].astype(str).isin([str(g) for g in existing_gids])]
    
    for _, row in missing_games.iterrows():
        conn.execute(text("""
            INSERT INTO games (game_id, game_date, season_id)
            VALUES (:gid, :gdate, :sid) ON CONFLICT (game_id) DO NOTHING
        """), {"gid": str(row['GAME_ID']), "gdate": row['GAME_DATE'], "sid": str(row['SEASON_YEAR'])})

def sync_statsbet_tables(season='2025-26'):
    print(f"🚀 Iniciando sincronización de StatsBet para la temporada {season}...")
    try:
        # Descarga inicial
        logs_request = playergamelogs.PlayerGameLogs(
            season_nullable=season,
            league_id_nullable='00',
            measure_type_player_game_logs_nullable='Base' 
        )
        all_logs = logs_request.get_data_frames()[0]

        if all_logs.empty:
            print("⚠️ No se obtuvieron datos de la API.")
            return

        # --- FILTRO CRÍTICO: Temporada Regular (002), Play-in (005) y Playoffs (004) ---
        # Excluimos Pretemporada (001) que te estaba dando problemas de FK
        valid_prefixes = ('002', '004', '005')
        logs = all_logs[all_logs['GAME_ID'].str.startswith(valid_prefixes)].copy()
        
        print(f"📊 Partidos filtrados: {len(logs)} (Regular, Play-in y Playoffs)")

        if logs.empty:
            print("⚠️ No hay partidos válidos tras el filtrado.")
            return

        # Cálculos de métricas
        logs['GAME_DATE'] = pd.to_datetime(logs['GAME_DATE'])
        logs['MIN_VAL'] = logs['MIN'].apply(lambda x: float(x) if x else 0.0)
        logs['TS_PCT'] = logs['PTS'] / (2 * (logs['FGA'] + 0.44 * logs['FTA'])).replace(0, np.nan)
        logs['TS_PCT'] = logs['TS_PCT'].fillna(0)

        player_trends_data, mean_players_data = [], []

        for pid, group in logs.groupby('PLAYER_ID'):
            group = group.sort_values('GAME_DATE', ascending=False)
            
            # Tendencias de temporada
            s = {
                'pid': pid, 'ap': group['PTS'].mean(), 'mp': group['PTS'].median(), 'sp': group['PTS'].std(),
                'aa': group['AST'].mean(), 'ma': group['AST'].median(), 'sa': group['AST'].std(),
                'ar': group['REB'].mean(), 'mr': group['REB'].median(), 'sr': group['REB'].std(),
                'as': group['STL'].mean(), 'ms': group['STL'].median(), 'ss': group['STL'].std(),
                'ab': group['BLK'].mean(), 'mb': group['BLK'].median(), 'sb': group['BLK'].std(),
                'at': group['TOV'].mean(), 'mt': group['TOV'].median(), 'st': group['TOV'].std(),
                'a3': group['FG3M'].mean(), 'm3': group['FG3M'].median(), 's3': group['FG3M'].std(),
                'afg': group['FG_PCT'].mean(), 'mfg': group['FG_PCT'].median(), 'sfg': group['FG_PCT'].std(),
                'aft': group['FT_PCT'].mean(), 'mft': group['FT_PCT'].median(), 'sft': group['FT_PCT'].std(),
                'apf': group['PF'].mean(), 'mpf': group['PF'].median(), 'spf': group['PF'].std(),
                'mpts': int(group['PTS'].mode()[0]) if not group['PTS'].mode().empty else 0,
                'gp': len(group), 'dd': any((group['PTS'] >= 10) & (group['REB'] >= 10)),
                'td': any((group['PTS'] >= 10) & (group['REB'] >= 10) & (group['AST'] >= 10))
            }
            player_trends_data.append(clean_data(s))

            # Media L5
            l5 = group.head(5)
            if not l5.empty:
                last_game = l5.iloc[0]
                prev_game = group.iloc[1] if len(group) > 1 else None
                days_rest = (last_game['GAME_DATE'] - prev_game['GAME_DATE']).days if prev_game is not None else 4
                mp_stats = {
                    'gid': last_game['GAME_ID'], 'pid': pid, 'tid': last_game['TEAM_ID'],
                    'gdt': last_game['GAME_DATE'], 'sid': season, 'pts': l5['PTS'].mean(),
                    'ast': l5['AST'].mean(), 'reb': l5['REB'].mean(), 'min': l5['MIN_VAL'].mean(),
                    'three': l5['FG3M'].mean(), 'pm': l5['PLUS_MINUS'].mean(), 'ts': l5['TS_PCT'].mean(),
                    'rest': min(days_rest, 4), 'b2b': days_rest == 1, 'fga': l5['FGA'].mean()
                }
                mean_players_data.append(clean_data(mp_stats))

        with engine.begin() as conn:
            ensure_players_exist(conn, logs)
            ensure_games_exist(conn, logs)

            print("🧹 Limpiando tablas de métricas...")
            conn.execute(text("TRUNCATE player_trends, mean_players RESTART IDENTITY CASCADE;"))

            print(f"📥 Insertando registros en player_trends ({len(player_trends_data)}) y mean_players ({len(mean_players_data)})...")
            
            # Inserción player_trends
            conn.execute(text("""
                INSERT INTO player_trends (
                    player_id, avg_points, med_points, std_points, avg_assists, med_assists, std_assists,
                    avg_rebounds, med_rebounds, std_rebounds, avg_steals, med_steals, std_steals,
                    avg_blocks, med_blocks, std_blocks, avg_turnovers, med_turnovers, std_turnovers,
                    avg_three_p_made, med_three_p_made, std_three_p_made, avg_field_goal_percentage,
                    med_field_goal_percentage, std_field_goal_percentage, avg_free_throws_percentage,
                    med_free_throws_percentage, std_free_throws_percentage, avg_personal_fouls,
                    med_personal_fouls, std_personal_fouls, games_played, has_double_double,
                    has_triple_double, mode_points, last_updated
                ) VALUES (
                    :pid, :ap, :mp, :sp, :aa, :ma, :sa, :ar, :mr, :sr, :as, :ms, :ss, :ab, :mb, :sb,
                    :at, :mt, :st, :a3, :m3, :s3, :afg, :mfg, :sfg, :aft, :mft, :sft, :apf, :mpf, :spf,
                    :gp, :dd, :td, :mpts, CURRENT_TIMESTAMP
                )
            """), player_trends_data)

            # Inserción mean_players
            conn.execute(text("""
                INSERT INTO mean_players (
                    game_id, player_id, team_id, game_date, l5_pts_avg, l5_ast_avg, l5_reb_avg,
                    l5_min_avg, l5_three_p_made_avg, l5_plus_minus_avg, l5_ts_pct_avg,
                    days_rest, is_b2b, avg_fga_l5, season_id, created_at, last_updated
                ) VALUES (
                    :gid, :pid, :tid, :gdt, :pts, :ast, :reb, :min, :three, :pm, :ts, 
                    :rest, :b2b, :fga, :sid, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                )
            """), mean_players_data)
            
        print("✅ Sincronización exitosa (Solo Regular, Play-in y Playoffs).")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    sync_statsbet_tables()