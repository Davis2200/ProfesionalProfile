import streamlit as st
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time 
import subprocess
import sys
import socket

# Cargar el .env (localmente) o Secrets (en Streamlit Cloud)
load_dotenv()

# 1. CONFIGURACIÓN DE URL DINÁMICA
# Prioridad: 1. Variable de entorno 'API_HOST' | 2. 'API_URL' del .env | 3. Localhost (Fallback)
env_api_url = os.getenv("API_URL", "http://192.168.0.82:8000")
api_host = os.gethostbyname(os.getenv("DB_HOST"))


# --- INICIAR API EN SEGUNDO PLANO ---
@st.cache_resource
def iniciar_api():
    # Buscamos la ruta de tu main.py de la API
    # Ajusta esta ruta según donde esté parado el servidor
    api_path = "assets/projects/nba_project/api/main.py" 
    
    # Ejecutamos uvicorn como un proceso independiente
    proc = subprocess.Popen([sys.executable, api_path])
    time.sleep(2) # Esperamos a que la API cargue
    return proc

# Llamamos a la función para que la API corra siempre
iniciar_api()

if api_host:
    # Si definiste API_HOST (ej: la IP de tu VM), la usamos con el puerto 8000
    base_url = f"http://{api_host}:8000"
else:
    # Si no, usamos la API_URL completa del .env
    base_url = env_api_url.rstrip('/')

# 2. CONFIGURACIÓN DE PÁGINA Y ESTILOS
st.set_page_config(page_title="StatsBet NBA", layout="wide")

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

# 3. LÓGICA DE NAVEGACIÓN
if 'fecha_consulta' not in st.session_state:
    st.session_state.fecha_consulta = datetime.now().date()

def set_fecha(nueva_fecha):
    st.session_state.fecha_consulta = nueva_fecha

# 4. UI - HEADER Y FILTROS
st.markdown('<div class="main-header"><div class="logo">STATS<span>BET</span></div></div>', unsafe_allow_html=True)

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

# 5. PETICIÓN A LA API
fecha_str = st.session_state.fecha_consulta.strftime("%Y-%m-%d")
full_api_url = f"{base_url}/predictions/calendar?target_date={fecha_str}"

try:
    # Timeout de 5 segundos para que la app no se quede colgada si tu VM está apagada
    res = requests.get(full_api_url, timeout=5)
    
    if res.status_code == 200:
        data = res.json()
        partidos = data.get("games", [])
        
        if not partidos:
            st.warning(f"No hay juegos programados para el {fecha_str}")
        else:
            for p in partidos:
                render_game_card(p)
    else:
        st.error(f"⚠️ Error de la API (Código {res.status_code})")
        with st.expander("Ver detalle del error"):
            st.json(res.json())

except requests.exceptions.ConnectTimeout:
    st.error(f"❌ Tiempo de espera agotado. La API en {base_url} no responde.")
except requests.exceptions.ConnectionError:
    st.error(f"❌ Conexión rechazada. Verifica que Uvicorn esté corriendo en {base_url}")
except Exception as e:
    st.error(f"❌ Error inesperado: {e}")