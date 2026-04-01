import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# 1. CARGA DEL DATASET GENERADO
df = pd.read_csv('features_scaled.csv', index_col='id_cliente')

# 2. PREPARACIÓN DE MATRICES
X = df.drop('target_fuga', axis=1)
y = df['target_fuga']

# Dividir en entrenamiento y prueba (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. CONFIGURACIÓN DE XGBOOST PARA EVITAR SOBREAJUSTE
# scale_pos_weight: Ajusta el peso si hay pocos casos de fuga (desbalance)
# max_depth: Controla la complejidad del árbol (3-5 es ideal para evitar memorización)
# eta (learning rate): Paso pequeño para un aprendizaje más robusto
# gamma: Penaliza la creación de nuevos nodos
model_xgb = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=1,
    reg_lambda=10,
    scale_pos_weight=(len(y) - sum(y)) / sum(y), 
    use_label_encoder=False,
    eval_metric='logloss',
    early_stopping_rounds=20 # Detiene el entrenamiento si deja de mejorar en el test
)

# 4. ENTRENAMIENTO CON VALIDACIÓN CRUZADA INTERNA
model_xgb.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

# 5. ESTIMACIÓN DE LA IMPORTANCIA DE LAS VARIABLES (PESOS)
importancias = pd.DataFrame({
    'Variable': X.columns,
    'Importancia': model_xgb.feature_importances_
}).sort_values(by='Importancia', ascending=False)

# 6. EVALUACIÓN DE DESEMPEÑO
y_pred = model_xgb.predict(X_test)
y_proba = model_xgb.predict_proba(X_test)[:, 1]

print("--- IMPORTANCIA DE LAS VARIABLES (PESOS DEL MODELO) ---")
print(importancias)
print("\n--- REPORTE DE CLASIFICACIÓN ---")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

# 7. GUARDAR MODELO PARA LA INTERFAZ
model_xgb.save_model('modelo_fuga_final.json')