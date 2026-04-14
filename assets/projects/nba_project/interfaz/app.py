import streamlit as st
import requests
import os
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="StatsBet NBA", layout="wide")

# 2. CARGA DE ESTILOS (CSS)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "assets", "style.css")

if os.path.exists(css_path):
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_game_card(p):
    """Genera el HTML de la tarjeta con estilo Cyberpunk"""
    marcador = f"{p['pts_l']} - {p['pts_v']}" if p['pts_l'] > 0 else p['hora']
    
    st.markdown(f"""
    <div class="game-card">
        <div class="card-header-meta">
            <span>{p['f_corta']}</span>
            <span class="arena-tag">{p['estadio']}</span>
            <span class="status-badge">{p['status'].upper()}</span>
        </div>
        <div class="vs-container">
            <div class="team-container">
                <div class="team-circle">
                    <img src="https://cdn.nba.com/logos/nba/{p['h_id']}/global/L/logo.svg">
                </div>
                <span class="team-label">{p['local']}</span>
            </div>
            <div class="score-box">{marcador}</div>
            <div class="team-container">
                <div class="team-circle">
                    <img src="https://cdn.nba.com/logos/nba/{p['v_id']}/global/L/logo.svg">
                </div>
                <span class="team-label">{p['visitante']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# 3. LÓGICA DE NAVEGACIÓN (Control de Fechas)
# Usamos session_state para que la página "recuerde" qué día estamos viendo
if 'fecha_consulta' not in st.session_state:
    st.session_state.fecha_consulta = datetime.now().date()

def set_fecha(nueva_fecha):
    st.session_state.fecha_consulta = nueva_fecha

# 4. HEADER Y BARRA DE FILTROS (Ayer, Hoy, Mañana)
st.markdown('<div class="main-header"><div class="logo">STATS<span>BET</span></div></div>', unsafe_allow_html=True)

# Creamos los 3 botones superiores
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⏪ AYER", use_container_width=True):
        set_fecha(datetime.now().date() - timedelta(days=1))
with col2:
    if st.button("🎯 HOY", use_container_width=True):
        set_fecha(datetime.now().date())
with col3:
    if st.button("⏩ MAÑANA", use_container_width=True):
        set_fecha(datetime.now().date() + timedelta(days=1))

# Dentro del bloque de petición a la API
fecha_str = st.session_state.fecha_consulta.strftime("%Y-%m-%d")
url = f"http://10.100.68.12:8000/predictions/calendar?target_date={fecha_str}"

try:
    res = requests.get(url)
    
    if res.status_code == 200:
        data = res.json()
        partidos = data.get("games", [])
        
        if not partidos:
            st.warning(f"No hay juegos programados para el {fecha_str}")
        else:
            for p in partidos:
                render_game_card(p)
    else:
        # Esto te dirá si el error es 404 (No encontrado) o 500 (Error interno)
        st.error(f"Error de la API: Código {res.status_code}")
        st.json(res.json()) # Muestra el detalle del error que envía FastAPI

except requests.exceptions.ConnectionError:
    st.error("❌ No se pudo conectar con el servidor. ¿Está encendido uvicorn?")
except Exception as e:
    st.error(f"❌ Error inesperado: {e}")