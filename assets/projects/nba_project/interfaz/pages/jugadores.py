import streamlit as st
import requests
import os

# 1. Carga de CSS específico de jugadores
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(os.path.dirname(BASE_DIR), "assets", "jugadores.css")

if os.path.exists(css_path):
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_player_card(p):
    img_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{p['id']}.png"
    categoria = st.session_state.get('p_cat', 'top_scorers')

    # Construimos el contenido del footer dinámicamente
    if categoria == "top_scorers":
        # Caso simple para anotadores
        pts_last = p.get('last_game_points', '0')
        footer_content = f"PTS: {pts_last}"
    else:
        # CASO DINÁMICO: Mapeamos los logros reales traídos por la API
        # Esto genera: "12 REB | 10 AST" o "15 PTS | 11 BLK" según sea el caso
        achievements = p.get('achievements', [])
        footer_content = " | ".join([f"{a['value']} {a['label']}" for a in achievements])

    st.markdown(f"""
    <div class="player-card">
        <div class="player-header">
            <div class="img-container">
                <img src="{img_url}" onerror="this.src='https://stats.nba.com/media/img/no-headshot.png'">
            </div>
            <div class="player-info">
                <div class="player-name">{p['name']}</div>
                <div class="pred-tag">PRÓXIMA PRED: <span>{p['prediction']} PTS</span></div>
            </div>
        </div>
        <div class="stats-grid">
            <div class="stat-box"><small>PROM</small><div>{p['stats']['Promedio']}</div></div>
            <div class="stat-box"><small>MED</small><div>{p['stats']['Mediana']}</div></div>
            <div class="stat-box"><small>MODA</small><div>{p['stats']['Moda']}</div></div>
            <div class="stat-box"><small>DESV</small><div>{p['stats']['Desviación']}</div></div>
        </div>
        <div class="player-footer" style="border-top: 1px solid #00d4ff55; color: #00d4ff; font-weight: bold;">
            LOGROS DETECTADOS: <span style="color: #fff; text-transform: uppercase;">{footer_content if footer_content else "N/A"}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)    
    
# Header
st.markdown('<div class="main-header"><div class="logo">STATS<span>BET</span> | PLAYERS</div></div>', unsafe_allow_html=True)

# Buscador
search_query = st.text_input("", placeholder="🔍 BUSCAR JUGADOR POR NOMBRE...")

# Tabs de navegación (Estado)
if 'p_cat' not in st.session_state: st.session_state.p_cat = "top_scorers"

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔥 TOP ANOTADORES", use_container_width=True): st.session_state.p_cat = "top_scorers"
with c2:
    if st.button("🌟 DOUBLE-DOUBLES", use_container_width=True): st.session_state.p_cat = "double_doubles"
with c3:
    if st.button("👑 TRIPLE-DOUBLES", use_container_width=True): st.session_state.p_cat = "triple_doubles"

# Llamada a la API
try:
    res = requests.get("http://127.0.0.1:8000/players/highlights", params={"search": search_query})
    if res.status_code == 200:
        data = res.json()
        players = data.get(st.session_state.p_cat, [])
        
        if not players:
            st.info("No hay datos para mostrar en esta categoría.")
        else:
            cols = st.columns(2)
            for i, p in enumerate(players):
                with cols[i % 2]:
                    render_player_card(p)
    else:
        st.error("Error al conectar con la API")
except Exception as e:
    st.error(f"Error de red: {e}")