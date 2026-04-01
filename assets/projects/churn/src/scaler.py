import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

def ejecutar_escalamiento(archivo_entrada, archivo_salida_datos, archivo_salida_escalador):
    # 1. Cargar el resultado de la ingeniería de características
    df = pd.read_csv("features_engineered.csv", index_col='id_cliente')
    
    # 2. Separar el Target (No se escala el target 0/1)
    X = df.drop('target_fuga', axis=1)
    y = df['target_fuga']
    
    # 3. Configurar el Escalador
    # Usamos StandardScaler para que la media sea 0 y desviación 1
    scaler = StandardScaler()
    
    # 4. Ajustar y Transformar
    X_scaled = pd.DataFrame(
        scaler.fit_transform(X),
        columns=X.columns,
        index=X.index
    )
    
    # 5. Reincorporar el Target
    df_escalado = X_scaled.join(y)
    
    # 6. Guardar los datos escalados para el script del modelo
    df_escalado.to_csv(archivo_salida_datos)
    
    # 7. GUARDAR EL OBJETO ESCALADOR (Fundamental para la App)
    # Sin este archivo, la interfaz no podrá procesar datos nuevos
    joblib.dump(scaler, archivo_salida_escalador)
    
    print(f"Escalamiento completado.")
    print(f"Datos guardados en: {archivo_salida_datos}")
    print(f"Objeto escalador guardado en: {archivo_salida_escalador}")

if __name__ == "__main__":
    ejecutar_escalamiento(
        archivo_entrada='features_engineered.csv',
        archivo_salida_datos='features_scaled.csv',
        archivo_salida_escalador='scaler_model.pkl'
    )