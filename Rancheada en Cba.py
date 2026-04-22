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

# --- INVENTARIO ---
ITEMS = {
    "celu": {"nombre": "Celular", "bono_stat": None, "bono_valor": 0, "desc": "Un celular cualquier"},
    "cuchillo": {"nombre": "Cuchillo", "bono_stat": "Calle", "bono_valor": 2, "desc": "Para defenderte"},
    "baterias": {"nombre": "Baterías", "bono_stat": None, "bono_valor": 0, "desc": "Pila para el瘾"},
    "gorra": {"nombre": "Gorra", "bono_stat": "Carisma", "bono_valor": 1, "desc": "Para pasar desapercibido"},
    "pañuelo": {"nombre": "Pañuelo", "bono_stat": None, "bono_valor": 0, "desc": "Para cubrirse la cara"},
    "fotos": {"nombre": "Fotos", "bono_stat": "Chamullo", "bono_valor": 2, "desc": "Evidencia para negociar"},
    "balanza": {"nombre": "Balanza", "bono_stat": None, "bono_valor": 0, "desc": "Pesa de verdad"},
    "luces": {"nombre": "Luces LED", "bono_stat": "Calle", "bono_valor": 1, "desc": "Para el vibe"},
    "piedrita": {"nombre": "Piedrita Blanca", "bono_stat": "Calle", "bono_valor": 3, "desc": "Para lanzar"},
}

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
            .vago-card-low-life {
                animation: vitalPulse 1s ease-in-out infinite;
            }
            @keyframes vitalPulse {
                0%, 100% { box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); }
                50% { box-shadow: 0 8px 32px 0 rgba(255, 0, 0, 0.6); border-left-color: #ff0000 !important; }
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
    if "volumen" not in st.session_state:
        st.session_state.volumen = 0.5

    # Control de volumen
    col_vol, col_mute = st.columns([3, 1])
    with col_vol:
        st.session_state.volumen = st.slider("🔊 Volumen", 0.0, 1.0, st.session_state.volumen, key="vol_slider")
    with col_mute:
        if st.button("🔇"):
            st.session_state.musica_activada = False
            st.rerun()

    # Actualizar volumen en JS
    comp_js = f"<script>window.setMusicVolume && window.setMusicVolume({st.session_state.volumen});</script>"
    components.html(comp_js, height=0, width=0)

    if not st.session_state.musica_activada:
        if st.button("🔊 Reproducir Música"):
            st.session_state.musica_activada = True
            st.rerun()
    else:
        # Usar el mismo audio del sistema global
        audio_codigo = """
        <script>
        var m = document.getElementById('musica-loop');
        if (m) {
            m.volume = %f;
            m.play().catch(() => {});
        }
        </script>
        """ % st.session_state.volumen
        components.html(audio_codigo, height=0, width=0)
        st.caption("🎵 Reproduciendo...")

    st.title("🏙️ RANCHADA EN CÓRDOBA")
    st.write("Armá tu banda para salir a dar una vuelta.")

    nombre = st.text_input("Apodo:")
    onda = st.selectbox("Elegí tu onda:", list(ONDAS_INFO.keys()), key="selector_onda")
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
        col_banda, col_inv, col_accion = st.columns([1, 1, 2])

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
                    # Vida baja = animación de parpadeo rojo
                    low_life = v["vida"] <= 40
                    card_class = "vago-card vago-card-low-life" if low_life else "vago-card"
                    color = "#ff3333" if v["vida"] <= 40 else "#00ffcc"
                    border_color = "#ff3333" if v["vida"] <= 40 else "#00ffcc"
                    st.markdown(
                        f"<div class='{card_class}' style='border-left-color: {border_color};'>"
                        f"<h4 style='margin:0; color:white; font-size:1.2em;'>{v['nombre']}</h4>"
                        f"<span style='color:{color}; font-weight: bold; font-size:1.1em;'>❤️ Vida: {v['vida']}%</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

        # --- COLUMNA INVENTARIO ---
        with col_inv:
            st.subheader("🎒 Equipado")
            if "inventario" not in st.session_state:
                st.session_state.inventario = []
            
            if st.session_state.inventario:
                for item_id in st.session_state.inventario:
                    item = ITEMS.get(item_id, {})
                    nombre = item.get("nombre", item_id)
                    stat = item.get("bono_stat")
                    bonus = item.get("bono_valor")
                    if stat:
                        st.markdown(
                            f"<div class='vago-card'>"
                            f"<h4 style='margin:0; color:#ffd700;'>{nombre}</h4>"
                            f"<span style='color:#888; font-size:0.9em;'>+{bonus} {stat}</span>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<div class='vago-card'>"
                            f"<h4 style='margin:0; color:#ffd700;'>{nombre}</h4>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
            else:
                st.caption("Sin items aún")

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

                # Tooltip con diff (dificultad) en cada opción
                info_onda = ONDAS_INFO.get(vago["onda"])
                stat_onda = info_onda["bono_stat"]
                bonus_onda = info_onda["valor"] if stat_onda == opt["stat"] else 0
                
                # Calcular bonus de items
                items_equipped = st.session_state.get("inventario", [])
                bonus_items = 0
                for item_id in items_equipped:
                    item = ITEMS.get(item_id)
                    if item and item.get("bono_stat") == opt["stat"]:
                        bonus_items += item.get("bono_valor", 0)
                
                # Tooltip
                tooltip = f"⚔️ {opt['stat']} (Dificultad: {opt['diff']}) | Bono onda: +{bonus_onda} | Bono items: +{bonus_items}"
                btn_texto = f"{opt['texto']} | Diff: {opt['diff']} | {opt['stat']}"
                
                if st.button(btn_texto, key=f"btn_{i}_{ev['id']}", help=tooltip):
                    # Fix: aplicar TODOS los bonuses correctamente
                    tirada = random.randint(1, 20)
                    total = tirada + bonus_onda + bonus_items
                    exito = total >= opt["diff"]

                    st.session_state[llave_res] = {
                        "exito": exito,
                        "nombre_vago": vago["nombre"],
                        "texto": f"Tirada: {tirada} + Bono onda: {bonus_onda} + Bono items: {bonus_items} = {total} vs Diff: {opt['diff']}. " + (opt["ok"] if exito else opt["fail"])
                    }
                    
                    import re
                    
# Manejo de inventario y vida
                    if "inventario" not in st.session_state:
                        st.session_state.inventario = []
                    
                    if not exito:
                        # Extraer daño del texto, ej: "(-60 Vida)" o "-20 Vida"
                        match_fail = re.search(r'-\s*(\d+)\s*Vida', opt["fail"], re.IGNORECASE)
                        dmg = int(match_fail.group(1)) if match_fail else 0
                        
                        # Extraer item si lo hay, ej: "[celu]" o "[cuchillo]"
                        match_item = re.search(r'\[(\w+)\]', opt["fail"])
                        item_encontrado = match_item.group(1) if match_item else None
                        
                        if item_encontrado and item_encontrado not in st.session_state.inventario:
                            st.session_state.inventario.append(item_encontrado)
                            st.toast(f"¡Encontraste: {ITEMS[item_encontrado]['nombre']}!")
                        
                        if dmg > 0:
                            vago["vida"] = max(0, vago["vida"] - dmg)
                    else:
                        # Extraer cura del texto si la hay, ej: "(+10 Vida)"
                        match_ok = re.search(r'\+\s*(\d+)\s*Vida', opt["ok"], re.IGNORECASE)
                        heal = int(match_ok.group(1)) if match_ok else 0
                        
                        # Extraer item si lo hay
                        match_item = re.search(r'\[(\w+)\]', opt["ok"])
                        item_encontrado = match_item.group(1) if match_item else None
                        
                        if item_encontrado and item_encontrado not in st.session_state.inventario:
                            st.session_state.inventario.append(item_encontrado)
                            st.toast(f"¡Encontraste: {ITEMS[item_encontrado]['nombre']}!")
                        
                        if heal > 0:
                            vago["vida"] = min(100, vago["vida"] + heal)

                    st.rerun()

            # PASO 3 — Mostrar resultado
            else:
                res = st.session_state[llave_res]
                st.caption(f"Actuó: {res['nombre_vago']}")
                if res["exito"]:
                    st.success(res["texto"])
                    # Play success sound
                    components.html("<script>window.playSuccessSound && window.playSuccessSound();</script>", height=0)
                else:
                    st.error(res["texto"])
                    # Play fail sound
                    components.html("<script>window.playFailSound && window.playFailSound();</script>", height=0)
                    for v in st.session_state.la_banda:
                        if v["vida"] <= 0:
                            st.warning(f"💀 {v['nombre']} quedó fuera de combate.")

                if st.button("Seguir caminando... 🚶"):
                    st.session_state.indice_evento += 1
                    st.rerun()
    else:
        mostrar_final()


def mostrar_derrota():
    st.markdown("""
        <style>
        .derrota-bg {
            background: linear-gradient(135deg, #1a0505 0%, #2d0000 50%, #0a0000 100%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid #ff3333;
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.3);
        }
        .derrota-titulo {
            color: #ff3333 !important;
            font-size: 2.5em;
            text-transform: uppercase;
            letter-spacing: 5px;
            text-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
        }
        .caido-card {
            background: rgba(255, 0, 0, 0.1);
            border-left: 4px solid #ff3333;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }
        .caido-nombre {
            color: #ff6666 !important;
            font-size: 1.3em;
            font-weight: bold;
        }
        .caido-onda {
            color: #888 !important;
            font-size: 0.9em;
        }
        </style>
        <div class="derrota-bg">
            <h1 class="derrota-titulo">⚠️ LA DOCTA SE LOS COMIÓ ⚠️</h1>
            <p style="color: #aaa; font-size: 1.2em;">La noche los escupió. No volvieron a casa.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Caídos en combate:")
    for v in st.session_state.la_banda:
        if v["vida"] <= 0:
            st.markdown(
                f"""<div class="caido-card">
                    <div class="caido-nombre">💀 {v['nombre']}</div>
                    <div class="caido-onda">{v['onda']}</div>
                </div>""",
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    if st.button("🔄 Reiniciar"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def mostrar_final():
    st.balloons()
    st.markdown("""
        <style>
        .final-bg {
            background: linear-gradient(135deg, #0a1a0a 0%, #00aa44 30%, #002200 100%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid #00ff66;
            box-shadow: 0 0 30px rgba(0, 255, 100, 0.3);
        }
        .final-titulo {
            color: #00ff66 !important;
            font-size: 2.5em;
            text-transform: uppercase;
            letter-spacing: 5px;
            text-shadow: 0 0 20px rgba(0, 255, 100, 0.8);
        }
        .sobreviviente-card {
            background: rgba(0, 255, 100, 0.1);
            border-left: 4px solid #00ff66;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }
        .vivo-nombre {
            color: #00ff66 !important;
            font-size: 1.3em;
            font-weight: bold;
        }
        </style>
        <div class="final-bg">
            <h1 class="final-titulo">🏆 SOBREVIVIERON 🏆</h1>
            <p style="color: #aaffaa; font-size: 1.2em;">La noche fue tough, pero volvieron.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Estado de la banda:")
    for v in st.session_state.la_banda:
        if v["vida"] <= 0:
            st.markdown(
                f"""<div class="caido-card" style="border-left-color: #444;">
                    <div class="caido-nombre" style="color: #666;">💀 {v['nombre']}</div>
                    <div class="caido-onda">{v['onda']} — Cayó</div>
                </div>""",
                unsafe_allow_html=True
            )
        else:
            icono = "🟢" if v["vida"] > 60 else "🟡" if v["vida"] > 20 else "🔴"
            st.markdown(
                f"""<div class="sobreviviente-card">
                    <div class="vivo-nombre">{icono} {v['nombre']}</div>
                    <div style="color: #888;">{v['onda']} — Vida: {v['vida']}%</div>
                </div>""",
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    if st.button("🔄 Jugar de nuevo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# --- SISTEMA DE AUDIO ---
AUDIO_ENABLED = True  # Master switch para audio

def play_sound(sound_name):
    """Reproduce un sonido desde Python usando JavaScript."""
    if not AUDIO_ENABLED:
        return
    js_code = f"<script>window.play{sound_name.capitalize()}Sound();</script>"
    components.html(js_code, height=0, width=0)

def inyectar_audio():
    """Inyecta el sistema de audio JS para UI sounds."""
    audio_js = """
    <audio id="sfx-hover" preload="auto">
        <source src="https://cdn.freesound.org/previews/612/612095_5674468-lq.mp3" type="audio/mpeg">
    </audio>
    <audio id="sfx-click" preload="auto">
        <source src="https://cdn.freesound.org/previews/320/320655_5260872-lq.mp3" type="audio/mpeg">
    </audio>
    <audio id="sfx-success" preload="auto">
        <source src="https://cdn.freesound.org/previews/459/459836_8210839-lq.mp3" type="audio/mpeg">
    </audio>
    <audio id="sfx-fail" preload="auto">
        <source src="https://cdn.freesound.org/previews/108/108958_1703281-lq.mp3" type="audio/mpeg">
    </audio>
    <audio id="sfx-toast" preload="auto">
        <source src="https://cdn.freesound.org/previews/256/256113_4559316-lq.mp3" type="audio/mpeg">
    </audio>
    <audio id="musica-loop" loop preload="auto">
        <source src="https://raw.githubusercontent.com/Viperino1997/Rancheada-en-la-Docta/main/intro.mp3" type="audio/mpeg">
    </audio>
    <script>
    const SFX = {
        hover: document.getElementById('sfx-hover'),
        click: document.getElementById('sfx-click'),
        success: document.getElementById('sfx-success'),
        fail: document.getElementById('sfx-fail'),
        toast: document.getElementById('sfx-toast')
    };
    
    function playSound(id) {
        const sfx = SFX[id];
        if (sfx) {
            sfx.currentTime = 0;
            sfx.play().catch(() => {});
        }
    }
    
    // Attach hover sounds a todos los botones de Streamlit
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            document.querySelectorAll('button[role="button"]').forEach(function(btn) {
                btn.addEventListener('mouseenter', function() {
                    if (!btn.disabled) playSound('hover');
                });
                btn.addEventListener('click', function() {
                    playSound('click');
                });
            });
            
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) {
                            node.querySelectorAll && node.querySelectorAll('button[role="button"]').forEach(function(btn) {
                                btn.addEventListener('mouseenter', function() {
                                    if (!btn.disabled) playSound('hover');
                                });
                                btn.addEventListener('click', function() {
                                    playSound('click');
                                });
                            });
                        }
                    });
                });
            });
            
            observer.observe(document.body, { childList: true, subtree: true });
        }, 500);
    });
    
    window.playHoverSound = function() { playSound('hover'); };
    window.playClickSound = function() { playSound('click'); };
    window.playSuccessSound = function() { playSound('success'); };
    window.playFailSound = function() { playSound('fail'); };
    window.playToastSound = function() { playSound('toast'); };
    
    // Control de volumen
    window.setMusicVolume = function(vol) {
        document.getElementById('musica-loop').volume = vol;
    };
    window.toggleMusic = function(on) {
        const m = document.getElementById('musica-loop');
        if (on) m.play().catch(() => {});
        else m.pause();
    };
    </script>
    """
    components.html(audio_js, height=0, width=0)


# --- ESTADO INICIAL ---
if 'pantalla' not in st.session_state:
    st.session_state.pantalla = "inicio"
if 'la_banda' not in st.session_state:
    st.session_state.la_banda = []

# --- INYECTAR AUDIO ---
inyectar_audio()

# --- RESTO DE ESTADOS ---
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
