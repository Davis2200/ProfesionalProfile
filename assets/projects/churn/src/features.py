import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. CARGA DE DATOS CRUDOS
df_raw = pd.read_csv('banca_transacciones.csv')

# 2. PIVOTEO DE DATOS (DE FORMATO LARGO A ANCHO)
df_pivot = df_raw.pivot(
    index='id_cliente', 
    columns='mes', 
    values=['saldo_mes', 'num_trx', 'tiene_nomina', 'quejas']
)

# Aplanar nombres de columnas: saldo_mes_t, num_trx_t-1, etc.
df_pivot.columns = [f'{col}_{mes}' for col, mes in df_pivot.columns]
df_pivot = df_pivot.reset_index()

# Recuperar el Target (Fuga)
target = df_raw.groupby('id_cliente')['target_fuga'].first().reset_index()
df_input = df_pivot.merge(target, on='id_cliente')

# 3. FUNCIÓN DE CÁLCULO DE TENDENCIAS (PENDIENTES)
def calcular_pendiente(serie):
    """Calcula el coeficiente de regresión para identificar dirección del comportamiento"""
    y = np.array(serie).reshape(-1, 1)
    X = np.array(range(len(serie))).reshape(-1, 1)
    return LinearRegression().fit(X, y).coef_[0][0]

# 4. CONSTRUCCIÓN DE CARACTERÍSTICAS DE ALTO VALOR
def construir_features_alto_valor(df):
    # Definir orden cronológico de columnas para transacciones
    cols_trx = ['num_trx_t-5', 'num_trx_t-4', 'num_trx_t-3', 'num_trx_t-2', 'num_trx_t-1', 'num_trx_t']
    
    features = pd.DataFrame(index=df['id_cliente'])
    
    # KPI 1: Momentum de Saldo (Ratio Actual vs Promedio Histórico)
    features['ratio_saldo_3m'] = df['saldo_mes_t'] / (df[['saldo_mes_t-1', 'saldo_mes_t-2', 'saldo_mes_t-3']].mean(axis=1) + 1)
    
    # KPI 2: Tendencia de Actividad (Pendiente de Transacciones)
    features['pendiente_actividad'] = df[cols_trx].apply(calcular_pendiente, axis=1)
    
    # KPI 3: Evento Detonante (Pérdida de Nómina entre t-1 y t)
    features['shifter_nomina'] = ((df['tiene_nomina_t-1'] == 1) & (df['tiene_nomina_t'] == 0)).astype(int)
    
    # KPI 4: Estabilidad de Ingresos (Coeficiente de Variación)
    features['volatilidad_transaccional'] = df[cols_trx].std(axis=1) / (df[cols_trx].mean(axis=1) + 1)
    
    # KPI 5: Índice de Fricción Acumulado (Pesando más lo reciente)
    features['friccion_ponderada'] = (df['quejas_t'] * 3) + (df['quejas_t-1'] * 1.5)
    
    # KPI 6: Variación Porcentual de Saldo (Último mes)
    features['pct_cambio_saldo_ultimo_mes'] = (df['saldo_mes_t'] - df['saldo_mes_t-1']) / (df['saldo_mes_t-1'] + 1)

    return features

# 5. GENERACIÓN DEL DATASET FINAL DE ENTRENAMIENTO
X = construir_features_alto_valor(df_input)
y = df_input.set_index('id_cliente')['target_fuga']

df_final_entrenamiento = X.join(y)

# 6. EXPORTACIÓN PARA EL MODELO
df_final_entrenamiento.to_csv('features_engineered.csv', index=True)

print("Ingeniería de características completada. Dataset guardado en 'features_engineered.csv'")