import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import plotly.express as px 
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Analizador de Retención", layout="wide")

# Obtener la ruta del directorio actual
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(CURRENT_DIR, "models")

def calcular_pendiente(serie):
    y = np.array(serie).reshape(-1, 1)
    X = np.array(range(len(serie))).reshape(-1, 1)
    return LinearRegression().fit(X, y).coef_[0][0]

@st.cache_resource
def cargar_artefactos():
    modelo = xgb.XGBClassifier()
    modelo_path = os.path.join(MODELS_DIR, "modelo_fuga_final.json")
    scaler_path = os.path.join(CURRENT_DIR, "scaler_model.pkl")
    
    modelo.load_model(modelo_path)
    scaler = joblib.load(scaler_path)
    return modelo, scaler

# --- 2. DISEÑO DE PANTALLA INICIAL ---
st.title("🏦 Panel de Análisis de Riesgo de Clientes")
st.markdown("Ingrese los datos transaccionales del cliente para generar el diagnóstico de fuga.")
st.divider()

# Creamos 3 columnas para organizar los inputs en la pantalla principal
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.subheader("💰 Historial de Saldos")
    s_t = st.number_input("Saldo Actual (t)", value=5000.0)
    s_t1 = st.number_input("Saldo Mes Anterior (t-1)", value=7000.0)
    s_t2 = st.number_input("Saldo (t-2)", value=8500.0)
    s_t3 = st.number_input("Saldo (t-3)", value=9000.0)

with col_b:
    st.subheader("📉 Actividad (Transacciones)")
    trx_t = st.slider("Mes t", 0, 50, 10)
    trx_t1 = st.slider("Mes t-1", 0, 50, 20)
    trx_t2 = st.slider("Mes t-2", 0, 50, 25)
    trx_t3 = st.slider("Mes t-3", 0, 50, 30)

with col_c:
    st.subheader("📎 Vinculación y Quejas")
    nom_t = st.selectbox("¿Tiene Nómina mes t?", [1, 0], index=1)
    nom_t1 = st.selectbox("¿Tenía Nómina mes t-1?", [1, 0], index=0)
    quejas_t = st.number_input("Quejas actuales (t)", 0, 5, 0)
    quejas_t1 = st.number_input("Quejas previas (t-1)", 0, 5, 1)

st.divider()

def mostrar_grafica_importancia(modelo, nombres_columnas):
    # Extraer importancias y ordenar
    importancias = modelo.feature_importances_
    df_imp = pd.DataFrame({
        'Variable': nombres_columnas,
        'Impacto': importancias
    }).sort_values(by='Impacto', ascending=True)

    # Crear gráfica con Plotly
    fig = px.bar(
        df_imp, 
        x='Impacto', 
        y='Variable', 
        orientation='h',
        title="<b>¿Qué está mirando el modelo para decidir?</b>",
        labels={'Impacto': 'Peso en la Decisión (0 a 1)', 'Variable': ''},
        color='Impacto',
        color_continuous_scale='RdYlGn_r' # Rojo para lo más importante
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    return df_imp


# --- 3. PROCESAMIENTO Y RESULTADOS ---
# Botón centrado
if st.button("🚀 GENERAR ANÁLISIS DE RIESGO", use_container_width=True):
    modelo, scaler = cargar_artefactos()
    
    # Ingeniería de Features
    data_input = {
        'ratio_saldo_3m': s_t / ((s_t1 + s_t2 + s_t3)/3 + 1),
        'pendiente_actividad': calcular_pendiente([trx_t3, trx_t2, trx_t1, trx_t]),
        'shifter_nomina': 1 if (nom_t1 == 1 and nom_t == 0) else 0,
        'volatilidad_transaccional': np.std([trx_t, trx_t1, trx_t2, trx_t3]) / (np.mean([trx_t, trx_t1, trx_t2, trx_t3]) + 1),
        'friccion_ponderada': (quejas_t * 3) + (quejas_t1 * 1.5),
        'pct_cambio_saldo_ultimo_mes': (s_t - s_t1) / (s_t1 + 1)
    }
    
    df_features = pd.DataFrame([data_input])
    features_escaladas = scaler.transform(df_features)
    
    # Predicción (con el fix de float nativo)
    probabilidad = float(modelo.predict_proba(features_escaladas)[0][1])

    st.divider()
    col_graph, col_txt = st.columns([1.5, 1])
    
    with col_graph:
        df_imp = mostrar_grafica_importancia(modelo, df_features.columns)
        
    with col_txt:
        st.subheader("🧐 Interpretación del Modelo")
        st.write("""
        Esta gráfica muestra los **Pesos de Importancia**. No son coeficientes lineales, 
        sino la capacidad de cada variable para reducir la incertidumbre del riesgo:
        """)
        
        # Interpretación dinámica basada en tu ranking real
        st.markdown(f"""
        1. **{df_imp.iloc[-1]['Variable']}**: Es el factor dominante. El modelo detecta que las variaciones bruscas aquí son la señal más clara de abandono.
        2. **{df_imp.iloc[-2]['Variable']}**: Actúa como un confirmador de la tendencia.
        3. **Variables Secundarias**: Aportan contexto para evitar falsos positivos.
        """)
    
    # --- ZONA DE RESULTADOS (Se refresca aquí) ---
    st.header("📋 Resultado del Diagnóstico")
    
    res_col1, res_col2 = st.columns([1, 2])
    
    with res_col1:
        # Indicador visual de color
        if probabilidad < 0.4:
            st.success(f"### RIESGO BAJO \n Probabilidad: {probabilidad*100:.1f}%")
        elif probabilidad < 0.7:
            st.warning(f"### RIESGO MODERADO \n Probabilidad: {probabilidad*100:.1f}%")
        else:
            st.error(f"### RIESGO CRÍTICO \n Probabilidad: {probabilidad*100:.1f}%")
        
        st.progress(probabilidad)

    with res_col2:
        st.info("**Factores de Comportamiento Detectados:**")
        
        # Lógica de interpretación de variables
        descripciones = []
        if data_input['shifter_nomina'] == 1:
            descripciones.append("🔴 **Alerta:** Se detectó la cancelación del depósito de nómina.")
        if data_input['ratio_saldo_3m'] < 0.7:
            descripciones.append("📉 **Tendencia:** El capital promedio del cliente está disminuyendo drásticamente.")
        if data_input['pendiente_actividad'] < -1:
            descripciones.append("📉 **Actividad:** El uso de la cuenta ha caído de forma constante.")
        if data_input['friccion_ponderada'] > 3:
            descripciones.append("⚠️ **Servicio:** El volumen de quejas reciente es inusual.")
        
        if not descripciones:
            st.write("✅ El comportamiento transaccional se mantiene dentro de los parámetros normales.")
        else:
            for item in descripciones:
                st.write(item)

    st.divider()
    # Recomendación Final
    st.subheader("🎯 Recomendación Estratégica")
    if probabilidad > 0.7:
        st.error("BLOQUEO DE FUGA: Contactar al cliente en las próximas 24 horas con una oferta de retención personalizada.")
    elif probabilidad > 0.4:
        st.warning("SEGUIMIENTO: Programar una llamada de fidelización y verificar motivos de insatisfacción.")
    else:
        st.success("FIDELIZACIÓN: Cliente estable. Incluir en campañas estándar de beneficios.")