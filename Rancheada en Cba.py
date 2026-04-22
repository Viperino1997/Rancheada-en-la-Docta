import json
import streamlit as st
import random
import streamlit.components.v1 as components
import base64

# --- DATOS ---
ONDAS_INFO = {
    "Estudiante de la Docta": {"bono_stat": "Carisma", "valor": 5, "desc": "+5 en Chamuyo"},
    "Vago de Barrio": {"bono_stat": "Calle", "valor": 5, "desc": "+5 en Aguante"},
    "Rapero de Compe": {"bono_stat": "Agilidad", "valor": 5, "desc": "+5 en Reacción"},
    "Vendedor de Panes Rellenos": {"bono_stat": "Chamullo", "valor": 7, "desc": "+7 en Labia Callejera"}
}

with open("eventos.json", "r", encoding="utf-8") as archivo:
    EVENTOS_NOCTURNOS = json.load(archivo)

# --- HELPERS ---
def banda_activa():
    """Devuelve solo los personajes que todavía tienen vida."""
    return [v for v in st.session_state.la_banda if v["vida"] > 0]

# --- ESTILOS ---
def aplicar_estilos(fase):
    if fase == "inicio":
        try:
            with open("C_map.png", "rb") as f:
                img_data = f.read()
            b64_img = base64.b64encode(img_data).decode()
            bg_url = f"data:image/png;base64,{b64_img}"
        except Exception:
            bg_url = "https://github.com/Viperino1997/Rancheada-en-la-Docta/blob/main/C_map.png?raw=true"
            
        css = """
            <style>
            .stApp {
                background-image: url("BG_URL_PLACEHOLDER");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
            h1, p, label { color: white !important; text-shadow: 2px 2px 4px #000000; }
            .stForm { background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; }
            </style>
        """.replace("BG_URL_PLACEHOLDER", bg_url)
        st.markdown(css, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
            
            /* Global Background */
            .stApp { 
                background: radial-gradient(circle at bottom right, #1a0b2e, #050505); 
                color: #e0e0e0;
            }
            
            /* Typography */
            h1, h2, h3 { 
                color: #00ffcc !important; 
                font-family: 'Outfit', sans-serif !important; 
                text-transform: uppercase;
                letter-spacing: 1.5px;
                text-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
            }
            p, div, label, span { 
                font-family: 'Outfit', sans-serif !important; 
            }
            
            /* Vago Card (Glassmorphism) */
            .vago-card {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-left: 5px solid #ff007f;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 12px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
                transition: transform 0.3s ease, box-shadow 0.3s ease, border-left-color 0.3s ease;
            }
            .vago-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 40px 0 rgba(255, 0, 127, 0.15);
            }
            .vago-card-dead {
                background: rgba(20, 20, 20, 0.5);
                border-left: 5px solid #444 !important;
                opacity: 0.6;
            }
            
            /* Buttons (Neon style) */
            .stButton>button { 
                background: linear-gradient(45deg, #ff007f, #7000ff);
                color: white !important; 
                border: none; 
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: bold;
                letter-spacing: 1px;
                box-shadow: 0 4px 15px rgba(255, 0, 127, 0.3);
                transition: all 0.3s ease;
                width: 100%;
            }
            .stButton>button:hover {
                box-shadow: 0 6px 20px rgba(112, 0, 255, 0.6);
                transform: scale(1.02);
            }
            
            /* Event Image Container */
            [data-testid="stImage"] img {
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.6);
                border: 1px solid rgba(0, 255, 204, 0.2);
                transition: transform 0.5s ease;
                margin-bottom: 15px;
            }
            [data-testid="stImage"] img:hover {
                transform: scale(1.01);
            }

            /* Event text box */
            .event-text {
                background: rgba(0, 255, 204, 0.05);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #00ffcc;
                font-size: 1.15rem;
                line-height: 1.6;
                margin-top: 15px;
                margin-bottom: 25px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
            
            /* Decorative divider */
            hr {
                border-color: rgba(255, 255, 255, 0.1);
                margin: 30px 0;
            }
            </style>
        """, unsafe_allow_html=True)

# --- PANTALLAS ---
def mostrar_inicio():
    if "musica_activada" not in st.session_state:
        st.session_state.musica_activada = False

    if not st.session_state.musica_activada:
        if st.button("🔊 Entrar con Música"):
            st.session_state.musica_activada = True
            st.rerun()
    else:
        audio_codigo = """
            <audio id="musica" loop autoplay>
                <source src="https://raw.githubusercontent.com/Viperino1997/Rancheada-en-la-Docta/main/intro.mp3" type="audio/mpeg">
            </audio>
            <script>document.getElementById("musica").play();</script>
        """
        components.html(audio_codigo, height=0, width=0)
        if st.button("🔇 Silenciar"):
            st.session_state.musica_activada = False
            st.rerun()

    st.title("🏙️ RANCHADA EN CÓRDOBA")
    st.write("Armá tu banda para salir a dar una vuelta.")

    nombre = st.text_input("Apodo:")
    onda = st.selectbox("Elegí tu onda:", list(ONDAS_INFO.keys()))
    st.info(f"**Habilidad Especial:** {ONDAS_INFO[onda]['desc']}")
    sumar = st.button("Sumar a la banda")

    if sumar:
        if nombre:
            st.session_state.la_banda.append({"nombre": nombre, "onda": onda, "vida": 100})
            st.toast(f"{nombre} está listo.")
            st.rerun()
        else:
            st.warning("¡Tenés que ingresar un apodo!")

    if st.session_state.la_banda:
        st.subheader("La Banda Actual:")
        for v in st.session_state.la_banda:
            st.write(f"• {v['nombre']} ({v['onda']})")

        if st.button("SALIR A PATEAR"):
            pool_eventos = EVENTOS_NOCTURNOS.copy()
            random.shuffle(pool_eventos)
            st.session_state.eventos_partida = pool_eventos
            st.session_state.indice_evento = 0
            st.session_state.pantalla = "en_la_calle"
            st.rerun()


def mostrar_calle():
    # Si toda la banda cayó, fin del juego
    if not banda_activa():
        mostrar_derrota()
        return

    if st.session_state.indice_evento < len(st.session_state.eventos_partida):
        ev = st.session_state.eventos_partida[st.session_state.indice_evento]
        st.title("🌙 LA NOCHE CORDOBESA")
        col_banda, col_accion = st.columns([1, 2])

        # --- COLUMNA BANDA ---
        with col_banda:
            st.subheader("Tu Banda")
            for v in st.session_state.la_banda:
                if v["vida"] <= 0:
                    st.markdown(
                        f"<div class='vago-card vago-card-dead'>"
                        f"<h4 style='margin:0; color:#888;'>{v['nombre']}</h4>"
                        f"<span style='color:#666; font-size:0.9em;'>💀 Fuera de combate</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                else:
                    color = "#ff007f" if v["vida"] <= 40 else "#00ffcc"
                    border_color = "#ff007f" if v["vida"] <= 40 else "#00ffcc"
                    st.markdown(
                        f"<div class='vago-card' style='border-left-color: {border_color};'>"
                        f"<h4 style='margin:0; color:white; font-size:1.2em;'>{v['nombre']}</h4>"
                        f"<span style='color:{color}; font-weight: bold; font-size:1.1em;'>❤️ Vida: {v['vida']}%</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        # --- COLUMNA ACCIÓN ---
        with col_accion:
            st.subheader(ev["titulo"])

            if "imagen" in ev:
                st.image(ev["imagen"], use_container_width=True)

            st.markdown(f"<div class='event-text'>{ev['relato']}</div>", unsafe_allow_html=True)
            st.markdown("<hr/>", unsafe_allow_html=True)

            llave_vago = f"vago_{ev['id']}"
            llave_res  = f"resuelto_{ev['id']}"

            # PASO 1 — Elegir quién actúa
            if llave_vago not in st.session_state:
                st.markdown("<h3 style='color: #fff; text-shadow: none;'>¿Quién se manda?</h3>", unsafe_allow_html=True)
                for v in banda_activa():
                    info_onda = ONDAS_INFO.get(v["onda"])
                    label = f"{v['nombre']} — {v['onda']} (bono en {info_onda['bono_stat']})"
                    if st.button(label, key=f"elegir_{v['nombre']}_{ev['id']}"):
                        st.session_state[llave_vago] = v["nombre"]
                        st.rerun()

            # PASO 2 — Elegir la acción
            elif llave_res not in st.session_state:
                nombre_vago = st.session_state[llave_vago]
                vago = next(v for v in st.session_state.la_banda if v["nombre"] == nombre_vago)
                info_onda = ONDAS_INFO.get(vago["onda"])
                st.info(f"Actuando: **{vago['nombre']}** ({vago['onda']})")

                for i, opt in enumerate(ev["opciones"]):
                    if st.button(opt["texto"], key=f"btn_{i}_{ev['id']}"):
                        valor_bono = info_onda["valor"] if info_onda["bono_stat"] == opt["stat"] else 0
                        tirada = random.randint(1, 20)
                        total = tirada + valor_bono
                        exito = total >= opt["diff"]

                        st.session_state[llave_res] = {
                            "exito": exito,
                            "nombre_vago": vago["nombre"],
                            "texto": f"Tirada: {tirada} + Bono: {valor_bono} = {total}. " + (opt["ok"] if exito else opt["fail"])
                        }
                        
                        import re
                        if not exito:
                            # Extraer daño del texto, ej: "(-60 Vida)" o "-20 Vida"
                            match_fail = re.search(r'-\s*(\d+)\s*Vida', opt["fail"], re.IGNORECASE)
                            dmg = int(match_fail.group(1)) if match_fail else 0
                            
                            # Si no se especificó daño pero antes restaba 20, 
                            # lo dejamos en 0 para que coincida exactamente con los textos.
                            # Algunos eventos como "Te dijo que no hay fiado" restarán 0.
                            if dmg > 0:
                                vago["vida"] = max(0, vago["vida"] - dmg)
                        else:
                            # Extraer cura del texto si la hay, ej: "(+10 Vida)"
                            match_ok = re.search(r'\+\s*(\d+)\s*Vida', opt["ok"], re.IGNORECASE)
                            heal = int(match_ok.group(1)) if match_ok else 0
                            if heal > 0:
                                vago["vida"] = min(100, vago["vida"] + heal)

                        st.rerun()

            # PASO 3 — Mostrar resultado
            else:
                res = st.session_state[llave_res]
                st.caption(f"Actuó: {res['nombre_vago']}")
                if res["exito"]:
                    st.success(res["texto"])
                else:
                    st.error(res["texto"])
                    for v in st.session_state.la_banda:
                        if v["vida"] <= 0:
                            st.warning(f"💀 {v['nombre']} quedó fuera de combate.")

                if st.button("Seguir caminando... 🚶"):
                    st.session_state.indice_evento += 1
                    st.rerun()
    else:
        mostrar_final()


def mostrar_derrota():
    st.error("💀 Toda la banda cayó. La Docta los comió vivos.")
    st.subheader("Estado final:")
    for v in st.session_state.la_banda:
        st.write(f"💀 **{v['nombre']}** ({v['onda']}) — Fuera de combate")
    if st.button("Volver a intentarlo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def mostrar_final():
    st.balloons()
    st.success("¡Sobrevivieron a la Docta!")
    st.subheader("Estado final de la banda:")
    for v in st.session_state.la_banda:
        if v["vida"] <= 0:
            st.write(f"💀 **{v['nombre']}** ({v['onda']}) — Cayó en combate")
        else:
            icono = "🟢" if v["vida"] > 60 else "🟡" if v["vida"] > 20 else "🔴"
            st.write(f"{icono} **{v['nombre']}** ({v['onda']}) — Vida: {v['vida']}%")

    if st.button("Volver a empezar"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# --- ESTADO INICIAL ---
if 'pantalla' not in st.session_state:
    st.session_state.pantalla = "inicio"
if 'la_banda' not in st.session_state:
    st.session_state.la_banda = []
if 'indice_evento' not in st.session_state:
    st.session_state.indice_evento = 0
if 'eventos_partida' not in st.session_state:
    st.session_state.eventos_partida = []

# --- MOTOR PRINCIPAL ---
aplicar_estilos(st.session_state.pantalla)

if st.session_state.pantalla == "inicio":
    mostrar_inicio()
elif st.session_state.pantalla == "en_la_calle":
    mostrar_calle()
else:
    mostrar_final()
