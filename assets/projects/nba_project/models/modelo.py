import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import joblib
import os
import sys

# Asegurar importación de la base de datos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import engine

def train_statsbet_model():
    print("🚀 Consultando Dataset desde la vista v_training_data...")
    
    # Consulta directa a la vista que ya tiene los joins y filtros
    query = "SELECT * FROM v_training_data"
    
    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"❌ Error al consultar la vista: {e}")
        return
    
    if df.empty or len(df) < 20:
        print("⚠️ No hay suficientes datos en la vista para entrenar. Revisa los filtros de temporada.")
        return

    # Definición de Features (deben coincidir con la vista)
    features = [
        'l5_pts_avg', 'l5_ast_avg', 'l5_reb_avg', 'l5_min_avg',
        'l5_ts_pct_avg', 'avg_fga_l5', 'days_rest', 
        'is_b2b', 'is_home', 'usage_rate'
    ]
    
    # Preparación de datos
    X = df[features].apply(pd.to_numeric, errors='coerce').fillna(0)
    y = pd.to_numeric(df['target_points'], errors='coerce')

    print(f"📊 Dataset cargado: {len(df)} registros para entrenamiento.")
    print("🤖 Entrenando modelo XGBoost...")

    # Configuración del modelo (Optimizada para evitar Overfitting)
    model = XGBRegressor(
        n_estimators=1000,
        learning_rate=0.03,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=3.0,     # Penalización L2 para regularizar
        reg_alpha=1.0,      # Penalización L1 para sparsity
        objective='reg:squarederror',
        random_state=42,
        n_jobs=-1
    )

    # Entrenamiento
    model.fit(X, y)

    # Guardar modelo y lista de features
    if not os.path.exists('models'):
        os.makedirs('models')
    
    model_data = {
        'model': model,
        'features': features,
        'metadata': {
            'trained_on_records': len(df),
            'season_id': '2025-26'
        }
    }
    
    joblib.dump(model_data, 'models/nba_points_models.pkl')
    print("✅ Modelo guardado en models/nba_points_models.pkl")

    # Mostrar importancia de variables
    importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    print("\n📈 Importancia de las variables en la predicción:")
    print(importances)

if __name__ == "__main__":
    train_statsbet_model()