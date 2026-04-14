import joblib
import pandas as pd
from sqlalchemy import text
from datetime import datetime
import sys 
import os 

# Configuración de ruta para database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import engine

def predict_next_games():
    # 1. Cargar el modelo guardado por el script de entrenamiento
    current_dir = os.path.dirname(__file__)
    # Buscamos en la carpeta 'models' que crea el script de entrenamiento
    model_path = os.path.join(current_dir, 'nba_points_models.pkl')
    
    if not os.path.exists(model_path):
        print(f"❌ Error: No se encuentra el modelo en {model_path}. ¿Ya corriste el entrenamiento?")
        return
        
    data_pack = joblib.load(model_path)
    model = data_pack['model']
    features_needed = data_pack['features']
    m_version = data_pack.get('metadata', {}).get('season_id', 'v2025-26')

    # 2. Buscar la fecha de los partidos (Hoy o el futuro más cercano)
    # Nota: Hoy es 13 de abril de 2026 según el sistema
    today = datetime.now().strftime('%Y-%m-%d')
    with engine.connect() as conn:
        res = conn.execute(text("SELECT MIN(game_date) FROM games WHERE game_date >= :today"), {"today": today}).fetchone()
        target_date = res[0]

    if not target_date:
        print("⚠️ No hay partidos programados próximamente.")
        return

    print(f"🏀 Generando predicciones StatsBet para la fecha: {target_date}")

    # 3. CONSULTA DE FEATURES: 
    # Unimos game_lineups con mean_players y player_advanced_metrics
    query = text("""
        SELECT 
            gl.player_id, gl.game_id, gl.team_id,
            latest_mp.l5_pts_avg, latest_mp.l5_ast_avg, latest_mp.l5_reb_avg, 
            latest_mp.l5_min_avg, latest_mp.l5_ts_pct_avg, latest_mp.avg_fga_l5, 
            latest_mp.days_rest, latest_mp.is_b2b::int,
            -- Priorizamos usage_rate de metrics, luego del promedio, luego 0
            COALESCE(pam.usage_rate, latest_mp.usage_rate_l5, 0) as usage_rate,
            CASE WHEN g.home_team_id = gl.team_id THEN 1 ELSE 0 END as is_home,
            COALESCE((SELECT ps.points FROM players_stats ps 
                      JOIN games g_old ON ps.game_id = g_old.game_id 
                      WHERE ps.player_id = gl.player_id AND g_old.game_date < :t_date
                      ORDER BY g_old.game_date DESC LIMIT 1), 0) as last_game_pts
        FROM game_lineups gl
        JOIN games g ON gl.game_id = g.game_id
        -- AQUÍ LA MAGIA: Buscamos el registro más reciente en mean_players
        LEFT JOIN LATERAL (
            SELECT * FROM mean_players mp 
            WHERE mp.player_id = gl.player_id 
              AND mp.game_date <= gl.game_date
            ORDER BY mp.game_date DESC 
            LIMIT 1
        ) latest_mp ON true
        LEFT JOIN player_advanced_metrics pam ON gl.player_id = pam.player_id AND gl.game_id = pam.game_id
        WHERE gl.game_date = :t_date
          AND gl.is_available = true;
    """)
    
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"t_date": target_date})

    if df.empty:
        print(f"⚠️ No hay registros en 'mean_players' para los jugadores del {target_date}.")
        print("💡 Consejo: Asegúrate de correr el script de sincronización de la API primero.")
        return

    # 4. Predicción
    # Nos aseguramos de que el orden de las columnas sea EXACTAMENTE el que el modelo espera
    X = df[features_needed].apply(pd.to_numeric, errors='coerce').fillna(0)
    df['predicted_points'] = model.predict(X)

    # 5. Guardar en player_predictions
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO player_predictions 
                (player_id, game_id, predicted_points, last_points, model_version, prediction_date)
                VALUES (:p_id, :g_id, :pred, :last, :ver, CURRENT_TIMESTAMP)
                ON CONFLICT (player_id, game_id) DO UPDATE SET 
                    predicted_points = EXCLUDED.predicted_points,
                    last_points = EXCLUDED.last_points,
                    model_version = EXCLUDED.model_version,
                    prediction_date = EXCLUDED.prediction_date;
            """), {
                "p_id": int(row['player_id']),
                "g_id": row['game_id'],
                "pred": round(float(row['predicted_points']), 1),
                "last": int(row['last_game_pts']),
                "ver": m_version
            })
            
    print(f"✅ Predicción finalizada: {len(df)} jugadores procesados.")
    print(f"📌 Resultados guardados en la tabla 'player_predictions'.")

if __name__ == "__main__":
    predict_next_games()