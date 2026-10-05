import base64
import random
import time
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
from supabase import Client, create_client


st.set_page_config(
    page_title="Jeu Imposteur",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="expanded",
)


if "code_chambre" not in st.session_state:
    st.session_state.code_chambre = None
if "pseudo" not in st.session_state:
    st.session_state.pseudo = ""

query_params = st.query_params
if "room" in query_params and not st.session_state.code_chambre:
    st.session_state.code_chambre = str(query_params["room"]).upper()


PALETTES = {
    "Kinich": {
        "full_name": "Kinich",
        "emoji": "🦖",
        "bg": "linear-gradient(135deg, #052e16 0%, #15803d 50%, #022c22 100%)",
        "primary": "#22c55e",
        "secondary": "#84cc16",
        "accent": "#16a34a",
        "text_title": "#86efac",
    },
    "Alhaitham": {
        "full_name": "Alhaitham",
        "emoji": "📖",
        "bg": "linear-gradient(135deg, #042f2e 0%, #0d9488 50%, #022c22 100%)",
        "primary": "#14b8a6",
        "secondary": "#5eead4",
        "accent": "#0f766e",
        "text_title": "#99f6e4",
    },
    "Kaveh": {
        "full_name": "Kaveh",
        "emoji": "🏛️️",
        "bg": "linear-gradient(135deg, #1c1917 0%, #3f2e18 50%, #1c1108 100%)",
        "primary": "#f59e0b",
        "secondary": "#fbbf24",
        "accent": "#b45309",
        "text_title": "#fef08a",
    },
    "Tighnari": {
        "full_name": "Tighnari",
        "emoji": "🦊",
        "bg": "linear-gradient(135deg, #082411 0%, #14401e 50%, #041408 100%)",
        "primary": "#84cc16",
        "secondary": "#a3e635",
        "accent": "#4d7c0f",
        "text_title": "#bef264",
    },
    "Venti": {
        "full_name": "Venti",
        "emoji": "🍃",
        "bg": "linear-gradient(135deg, #042f2e 0%, #0d5c56 50%, #021a19 100%)",
        "primary": "#14b8a6",
        "secondary": "#5eead4",
        "accent": "#0f766e",
        "text_title": "#99f6e4",
    },
    "Xiao": {
        "full_name": "Xiao",
        "emoji": "👹",
        "bg": "linear-gradient(135deg, #032024 0%, #084048 50%, #011215 100%)",
        "primary": "#06b6d4",
        "secondary": "#67e8f9",
        "accent": "#0e7490",
        "text_title": "#a5f3fc",
    },
    "Kazuha": {
        "full_name": "Kaedehara Kazuha",
        "emoji": "🍁",
        "bg": "linear-gradient(135deg, #2b110c 0%, #4a1f18 50%, #170805 100%)",
        "primary": "#f97316",
        "secondary": "#fca5a5",
        "accent": "#c2410c",
        "text_title": "#ffedd5",
    },
    "Wanderer": {
        "full_name": "Wanderer",
        "emoji": "🎓",
        "bg": "linear-gradient(135deg, #0a1b3a 0%, #0284c7 50%, #032b45 100%)",
        "primary": "#38bdf8",
        "secondary": "#7dd3fc",
        "accent": "#0284c7",
        "text_title": "#bae6fd",
    },
    "Varka": {
        "full_name": "Varka",
        "emoji": "🐺",
        "bg": "linear-gradient(135deg, #182232 0%, #29384c 50%, #0e141f 100%)",
        "primary": "#64748b",
        "secondary": "#94a3b8",
        "accent": "#334155",
        "text_title": "#e2e8f0",
    },
    "Lohen": {
        "full_name": "Lohen",
        "emoji": "❄️",
        "bg": "linear-gradient(135deg, #0c1a2b 0%, #1a2f47 50%, #050d17 100%)",
        "primary": "#38bdf8",
        "secondary": "#e2e8f0",
        "accent": "#0284c7",
        "text_title": "#f1f5f9",
    },
    "Wriothesley": {
        "full_name": "Wriothesley",
        "emoji": "🥊",
        "bg": "linear-gradient(135deg, #1c0a0e 0%, #3a151e 50%, #0f0407 100%)",
        "primary": "#e11d48",
        "secondary": "#fda4af",
        "accent": "#9f1239",
        "text_title": "#ffe4e6",
    },
    "Cyno": {
        "full_name": "Cyno",
        "emoji": "⚡",
        "bg": "linear-gradient(135deg, #210d33 0%, #3e1b5b 50%, #10051a 100%)",
        "primary": "#a855f7",
        "secondary": "#e9d5ff",
        "accent": "#6b21a8",
        "text_title": "#f3e8ff",
    },
    "Flins": {
        "full_name": "Flins",
        "emoji": "🪦",
        "bg": "linear-gradient(135deg, #02131d 0%, #092c3e 50%, #010a10 100%)",
        "primary": "#0284c7",
        "secondary": "#38bdf8",
        "accent": "#0369a1",
        "text_title": "#bae6fd",
    },
    "Mitya": {
        "full_name": "Mitya",
        "emoji": "🧪",
        "bg": "linear-gradient(135deg, #1e0b36 0%, #4c1d95 50%, #0f041d 100%)",
        "primary": "#a855f7",
        "secondary": "#e9d5ff",
        "accent": "#6b21a8",
        "text_title": "#f3e8ff",
    },
    "Valeriy": {
        "full_name": "Valeriy",
        "emoji": "🐻",
        "bg": "linear-gradient(135deg, #1f0a2e 0%, #3b0764 50%, #12031c 100%)",
        "primary": "#8b5cf6",
        "secondary": "#ddd6fe",
        "accent": "#6d28d9",
        "text_title": "#c4b5fd",
    },
    "Zhongli": {
        "full_name": "Zhongli",
        "emoji": "🪨",
        "bg": "linear-gradient(135deg, #261704 0%, #452c0a 50%, #140b01 100%)",
        "primary": "#d97706",
        "secondary": "#fde047",
        "accent": "#92400e",
        "text_title": "#fef08a",
    },
    "Albedo": {
        "full_name": "Albedo",
        "emoji": "🧪",
        "bg": "linear-gradient(135deg, #261f0d 0%, #45391d 50%, #141005 100%)",
        "primary": "#eab308",
        "secondary": "#fef08a",
        "accent": "#854d0e",
        "text_title": "#fef9c3",
    },
    "Neuvillette": {
        "full_name": "Neuvillette",
        "emoji": "⚖",
        "bg": "linear-gradient(135deg, #0b1a30 0%, #16325c 50%, #050d1a 100%)",
        "primary": "#2563eb",
        "secondary": "#93c5fd",
        "accent": "#1e40af",
        "text_title": "#dbeafe",
    },
    "Tartaglia": {
        "full_name": "Tartaglia",
        "emoji": "🏹",
        "bg": "linear-gradient(135deg, #2b1408 0%, #4a2814 50%, #170a03 100%)",
        "primary": "#ea580c",
        "secondary": "#fdba74",
        "accent": "#9a3412",
        "text_title": "#ffedd5",
    },
    "Lyney": {
        "full_name": "Lyney",
        "emoji": "🎩",
        "bg": "linear-gradient(135deg, #2e0811 0%, #4c111f 50%, #170308 100%)",
        "primary": "#e11d48",
        "secondary": "#fca5a5",
        "accent": "#9f1239",
        "text_title": "#ffe4e6",
    },
    "Gaming": {
        "full_name": "Gaming",
        "emoji": "🦁",
        "bg": "linear-gradient(135deg, #2e0d04 0%, #521a0a 50%, #170501 100%)",
        "primary": "#f97316",
        "secondary": "#fed7aa",
        "accent": "#c2410c",
        "text_title": "#ffedd5",
    },
    "Alyosha": {
        "full_name": "Alyosha",
        "emoji": "🐕",
        "bg": "linear-gradient(135deg, #0f172a 0%, #334155 50%, #020617 100%)",
        "primary": "#38bdf8",
        "secondary": "#94a3b8",
        "accent": "#0284c7",
        "text_title": "#e2e8f0",
    },
    "Durin": {
        "full_name": "Durin",
        "emoji": "🐉",
        "bg": "linear-gradient(135deg, #210306 0%, #42080f 50%, #120103 100%)",
        "primary": "#ef4444",
        "secondary": "#fca5a5",
        "accent": "#991b1b",
        "text_title": "#fecaca",
    },
    "Noy": {
        "full_name": "Noy",
        "emoji": "✨",
        "bg": "linear-gradient(135deg, #1e1308 0%, #3b2814 50%, #0f0903 100%)",
        "primary": "#d97706",
        "secondary": "#fcd34d",
        "accent": "#78350f",
        "text_title": "#fef3c7",
    },
}

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


supabase = init_supabase()


def generer_code():
    return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=4))


def afficher_compte_a_rebours(timer_end, accent_color, primary_color):
    """Affiche un timer fluide en JS qui rafraîchit automatiquement la page à 0s."""
    js_code = f"""
    <div id="timer-box" style="
        background-color: {accent_color};
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-size: 1.1rem;
        font-weight: bold;
        padding: 10px 16px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid {primary_color};
    ">
        ⏳ Temps restant : <span id="time-left">--</span>s
    </div>

    <script>
        const timerEnd = {timer_end};
        function updateTimer() {{
            const now = Math.floor(Date.now() / 1000);
            const remaining = Math.max(0, timerEnd - now);
            const elem = document.getElementById("time-left");
            if (elem) {{
                elem.innerText = remaining;
            }}
            if (remaining <= 0) {{
                window.parent.postMessage({{type: 'streamlit:rerun'}}, '*');
            }}
        }}
        updateTimer();
        setInterval(updateTimer, 1000);
    </script>
    """
    components.html(js_code, height=65)


def appliquer_style(theme_key):
    t = PALETTES.get(theme_key, PALETTES["Kinich"])
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');

        .stApp {{
            background: {t['bg']} !important;
            color: #f8fafc;
            font-family: 'Montserrat', sans-serif;
        }}

        h1 {{
            font-size: 2.2rem !important;
            font-weight: 900 !important;
            color: {t['text_title']} !important;
            text-transform: uppercase;
            text-align: center;
            margin: 0;
        }}

        h2, h3 {{
            color: {t['secondary']} !important;
            font-weight: 800 !important;
        }}

        .phrase-card {{
            background: rgba(255, 255, 255, 0.08);
            border: 2px solid {t['primary']};
            border-radius: 12px;
            padding: 20px;
            color: #ffffff !important;
            text-align: center;
            font-size: 1.4rem;
            font-weight: 700;
            margin: 15px 0;
        }}

        .revelation-card {{
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid {t['primary']};
            border-radius: 12px;
            padding: 20px;
            color: #ffffff !important;
            text-align: center;
            margin-top: 15px;
        }}

        .stButton > button {{
            border-radius: 10px !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, {t['primary']} 0%, {t['accent']} 100%) !important;
            color: #ffffff !important;
            padding: 0.6rem 1.2rem !important;
            border: none !important;
        }}

        .stTextInput input, .stTextArea textarea, div[data-baseweb="select"] input {{
            background-color: #ffffff !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }}

        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            color: #0f172a !important;
            border-radius: 8px !important;
        }}

        div[data-testid="stRadio"] label {{
            color: #ffffff !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stRadio"] p {{
            color: {t['secondary']} !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
        }}

        label {{
            color: #ffffff !important;
            font-weight: 700 !important;
        }}

        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 25px;
        }}

        .character-icon {{
            font-size: 4rem;
            text-align: center;
            margin-bottom: 10px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


if not st.session_state.code_chambre:
    appliquer_style("Kinich")

    st.markdown(
        f"""
        <div class='header-container'>
            <span style='font-size: 2.5rem;'>🎭</span>
            <h1>JEU IMPOSTEUR</h1>
            <span style='font-size: 2.5rem;'>🦎</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pseudo_raw = st.text_input("👤 Ton pseudo :", placeholder="Ex: Alex")
    pseudo_input = pseudo_raw.strip() if pseudo_raw else ""

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏠 CRÉER")
        if st.button("Lancer une partie", use_container_width=True):
            if pseudo_input:
                code = generer_code()
                theme_choisi = random.choice(list(PALETTES.keys()))

                supabase.table("rooms").insert(
                    {
                        "code": code,
                        "phase": "ATTENTE",
                        "timer_end": 0,
                        "theme": theme_choisi,
                        "host": pseudo_input,
                    }
                ).execute()
                supabase.table("players").insert(
                    {"room_code": code, "pseudo": pseudo_input}
                ).execute()

                st.session_state.pseudo = pseudo_input
                st.session_state.code_chambre = code
                st.rerun()
            else:
                st.error("Renseigne ton pseudo !")

    with col2:
        st.subheader("REJOINDRE")
        code_defaut = st.session_state.get("code_chambre", "")
        code_raw = st.text_input(
            "Code de chambre :", value=code_defaut if code_defaut else "", placeholder="Ex: ABCD"
        )
        code_input = code_raw.strip().upper() if code_raw else ""

        if st.button("Rejoindre la partie", use_container_width=True):
            if pseudo_input and code_input:
                room_check = (
                    supabase.table("rooms")
                    .select("*")
                    .eq("code", code_input)
                    .execute()
                )
                if room_check.data:
                    try:
                        supabase.table("players").insert(
                            {
                                "room_code": code_input,
                                "pseudo": pseudo_input,
                            }
                        ).execute()
                    except Exception:
                        pass

                    st.session_state.pseudo = pseudo_input
                    st.session_state.code_chambre = code_input
                    st.rerun()
                else:
                    st.error("Chambre introuvable !")
            else:
                st.error("Remplis tous les champs !")


else:
    code = st.session_state.code_chambre
    pseudo = st.session_state.pseudo

    res_room = (
        supabase.table("rooms")
        .select("*")
        .eq("code", code)
        .execute()
    )

    if not res_room.data:
        st.error("La salle n'existe plus.")
        st.session_state.code_chambre = None
        if st.button("Retour à l'accueil"):
            st.rerun()
    else:
        room_data = res_room.data[0]
        phase_actuelle = room_data.get("phase", "ATTENTE")
        timer_end = room_data.get("timer_end", 0)
        theme_key = room_data.get("theme", "Kinich")
        host_pseudo = room_data.get("host", "")

        char_info = PALETTES.get(theme_key, PALETTES["Kinich"])
        appliquer_style(theme_key)

        st.markdown(
            f"<div class='character-icon'>{char_info['emoji']}</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<h1>{char_info['full_name']}</h1>",
            unsafe_allow_html=True,
        )
        st.caption(f"Code de la salle : **{code}**")

        res_joueurs = (
            supabase.table("players")
            .select("pseudo")
            .eq("room_code", code)
            .execute()
        )
        liste_joueurs = [j["pseudo"] for j in res_joueurs.data]
        total_joueurs = len(liste_joueurs)

        st.sidebar.markdown("### Thème actuel")
        st.sidebar.markdown(f"**{char_info['emoji']} {char_info['full_name']}**")
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Joueurs en ligne")
        for j in liste_joueurs:
            if j == host_pseudo:
                st.sidebar.markdown(f"- **{j} 👑 (Hôte)**")
            else:
                st.sidebar.markdown(f"- **{j}**")

        if st.sidebar.button("🔄 Actualiser l'état"):
            st.rerun()

        if phase_actuelle == "ATTENTE":
            st.write("## ⏳ Salle d'attente")
            st.info(f"En attente des joueurs... ({total_joueurs} présent(s))")

            st.write("### Joueurs connectés :")
            for j in liste_joueurs:
                if j == host_pseudo:
                    st.write(f"- 👑 **{j}** (Créateur de la partie)")
                else:
                    st.write(f"- 👤 **{j}**")

            st.write("---")

            lien_partage = (
                f"https://impostor-game-multi.streamlit.app/?room={code}"
            )
            st.subheader("📲 Partager la salle avec vos amis")
            st.code(lien_partage, language=None)
            st.caption(
                "Copiez ce lien et envoyez-le sur WhatsApp ! Vos amis n'auront qu'à entrer leur pseudo."
            )

            st.write("---")

            if pseudo == host_pseudo:
                st.success(
                    "👑 Tu es l'hôte ! Clique ci-dessous pour démarrer dès que tout le monde est là."
                )
                if st.button("🚀 Lancer la partie", use_container_width=True):
                    supabase.table("rooms").update(
                        {
                            "phase": "ECRITURE",
                            "timer_end": int(time.time()) + 120,
                        }
                    ).eq("code", code).execute()
                    st.rerun()
            else:
                st.warning(f"Attendez que **{host_pseudo}** lance la partie...")

            components.html(
                """
                <script>
                    setTimeout(function(){
                        window.parent.postMessage({type: 'streamlit:rerun'}, '*');
                    }, 4000);
                </script>
                """,
                height=0,
            )

        elif phase_actuelle == "ECRITURE":
            afficher_compte_a_rebours(
                timer_end, char_info["accent"], char_info["primary"]
            )
            temps_restant = max(0, timer_end - int(time.time()))

            st.write("## ✍️ Étape 1 : Écrire une phrase")

            res_phrases = (
                supabase.table("phrases")
                .select("*")
                .eq("room_code", code)
                .execute()
            )
            nb_phrases_soumises = len(res_phrases.data)
            deja_soumis = any(p["auteur"] == pseudo for p in res_phrases.data)

            st.progress(min(1.0, nb_phrases_soumises / max(1, total_joueurs)))
            st.caption(
                f"Phrases soumises : {nb_phrases_soumises} / {total_joueurs}"
            )

            if temps_restant <= 0 or nb_phrases_soumises >= total_joueurs:
                phrases_non_jouees = [
                    p for p in res_phrases.data if not p.get("jouee")
                ]
                if phrases_non_jouees:
                    carte = random.choice(phrases_non_jouees)
                    supabase.table("phrases").update({"jouee": True}).eq(
                        "id", carte["id"]
                    ).execute()

                supabase.table("rooms").update(
                    {"phase": "VOTE", "timer_end": int(time.time()) + 120}
                ).eq("code", code).execute()
                st.rerun()

            if deja_soumis:
                st.info(
                    "✅ Ta phrase est enregistrée ! En attente des autres joueurs..."
                )
            else:
                cible = st.selectbox("Qui vises-tu ?", liste_joueurs)
                phrase_raw = st.text_area("Sa phrase typique :")
                phrase_clean = phrase_raw.strip() if phrase_raw else ""

                if st.button("Valider ma phrase", use_container_width=True):
                    if phrase_clean:
                        supabase.table("phrases").insert(
                            {
                                "room_code": code,
                                "auteur": pseudo,
                                "cible": cible,
                                "phrase": phrase_clean,
                                "jouee": False,
                            }
                        ).execute()
                        st.rerun()
                    else:
                        st.error("⚠ Écris une phrase pour valider !")

        elif phase_actuelle == "VOTE":
            afficher_compte_a_rebours(
                timer_end, char_info["accent"], char_info["primary"]
            )
            temps_restant = max(0, timer_end - int(time.time()))

            st.write("## 🎲 Étape 2 : Votez pour la cible !")

            carte_actuelle = (
                supabase.table("phrases")
                .select("*")
                .eq("room_code", code)
                .eq("jouee", True)
                .order("id", desc=True)
                .limit(1)
                .execute()
            )

            if carte_actuelle.data:
                carte = carte_actuelle.data[0]
                st.markdown(
                    f"<div class='phrase-card'>« {carte['phrase']} »</div>",
                    unsafe_allow_html=True,
                )

                res_votes = (
                    supabase.table("votes")
                    .select("*")
                    .eq("phrase_id", carte["id"])
                    .execute()
                )
                nb_votes = len(res_votes.data)
                deja_vote = any(v["votant"] == pseudo for v in res_votes.data)

                if temps_restant <= 0 or nb_votes >= total_joueurs:
                    supabase.table("rooms").update(
                        {"phase": "RESULTATS", "timer_end": int(time.time()) + 120}
                    ).eq("code", code).execute()
                    st.rerun()

                if deja_vote:
                    st.info(
                        "✅ Ton vote est validé ! En attente de la fin du temps..."
                    )
                else:
                    vote_choix = st.radio(
                        "Qui a écrit cette phrase ?", liste_joueurs
                    )
                    if st.button("Valider mon vote", use_container_width=True):
                        supabase.table("votes").upsert(
                            {
                                "phrase_id": carte["id"],
                                "votant": pseudo,
                                "cible_votee": vote_choix,
                            }
                        ).execute()
                        st.rerun()

        elif phase_actuelle == "RESULTATS":
            st.write("## 📊 Étape 3 : Révélation")

            carte_actuelle = (
                supabase.table("phrases")
                .select("*")
                .eq("room_code", code)
                .eq("jouee", True)
                .order("id", desc=True)
                .limit(1)
                .execute()
            )

            if carte_actuelle.data:
                carte = carte_actuelle.data[0]
                res_votes = (
                    supabase.table("votes")
                    .select("cible_votee")
                    .eq("phrase_id", carte["id"])
                    .execute()
                )

                if res_votes.data:
                    counts = {}
                    for v in res_votes.data:
                        c = v["cible_votee"]
                        counts[c] = counts.get(c, 0) + 1

                    fig, ax = plt.subplots(figsize=(5, 5))
                    fig.patch.set_facecolor("none")
                    ax.set_facecolor("none")

                    ax.pie(
                        counts.values(),
                        labels=counts.keys(),
                        autopct="%1.1f%%",
                        startangle=140,
                        textprops=dict(color="white", weight="bold"),
                    )
                    ax.axis("equal")
                    st.pyplot(fig)

                st.markdown(
                    f"""
                <div class='revelation-card'>
                    <h2>🎯 La Cible : {carte['cible']}</h2>
                    <h3> Auteur : {carte['auteur']}</h3>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.write("---")

                all_phrases = (
                    supabase.table("phrases")
                    .select("*")
                    .eq("room_code", code)
                    .execute()
                    .data
                )
                phrases_restantes = [p for p in all_phrases if not p.get("jouee")]

                if phrases_restantes:
                    if st.button("▶ Phrase suivante", use_container_width=True):
                        prochaine_carte = random.choice(phrases_restantes)
                        supabase.table("phrases").update({"jouee": True}).eq(
                            "id", prochaine_carte["id"]
                        ).execute()

                        theme_suivant = random.choice(list(PALETTES.keys()))
                        supabase.table("rooms").update(
                            {
                                "phase": "VOTE",
                                "timer_end": int(time.time()) + 120,
                                "theme": theme_suivant,
                            }
                        ).eq("code", code).execute()
                        st.rerun()

                else:
                    st.success("🎉 Toutes les phrases soumises ont été jouées !")
                    col_partie, col_quitter = st.columns(2)

                    with col_partie:
                        if st.button(
                            "Refaire une nouvelle partie",
                            use_container_width=True,
                        ):
                            supabase.table("phrases").delete().eq(
                                "room_code", code
                            ).execute()

                            theme_suivant = random.choice(list(PALETTES.keys()))
                            supabase.table("rooms").update(
                                {
                                    "phase": "ECRITURE",
                                    "timer_end": int(time.time()) + 120,
                                    "theme": theme_suivant,
                                }
                            ).eq("code", code).execute()
                            st.rerun()

                    with col_quitter:
                        if st.button(
                            "Quitter la partie", use_container_width=True
                        ):
                            st.session_state.code_chambre = None
                            st.rerun()

            st.write("---")
            st.subheader("🔗 Partager la partie")

            lien_partage = (
                f"https://impostor-game-multi.streamlit.app/?room={code}"
            )

            col_link, col_copy = st.columns([3, 1])
            with col_link:
                st.text_input(
                    "Lien :",
                    value=lien_partage,
                    disabled=True,
                    label_visibility="collapsed",
                )
            with col_copy:
                if st.button("Copier"):
                    st.toast("Lien copié !", icon="✅")

            if st.button("Quitter la salle"):
                st.session_state.code_chambre = None
                st.rerun()