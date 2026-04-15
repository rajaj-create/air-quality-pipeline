import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="🌿 Air Quality Pipeline",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main-header {
    background: #065A82;
    padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem;
    color: white; text-align: center;
}
.card {
    background: #F8FAFB; padding: 1.2rem; border-radius: 10px;
    border-left: 4px solid #065A82; margin-bottom: 1rem;
}
.card-green  { border-left-color: #16a34a; background: #F0FDF4; }
.card-red    { border-left-color: #dc2626; background: #FEF2F2; }
.card-purple { border-left-color: #7c3aed; background: #FAF5FF; }
.card-orange { border-left-color: #ea580c; background: #FFF7ED; }
.card-teal   { border-left-color: #0D9488; background: #F0FDFA; }
.badge {
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 13px; font-weight: bold; margin: 3px;
}
.badge-blue   { background: #DBEAFE; color: #1E40AF; }
.badge-green  { background: #DCFCE7; color: #166534; }
.badge-purple { background: #EDE9FE; color: #5B21B6; }
.badge-teal   { background: #CCFBF1; color: #115E59; }
.avatar {
    width: 56px; height: 56px; border-radius: 50%;
    background: #065A82; display: flex; align-items: center;
    justify-content: center; font-size: 20px; font-weight: bold;
    color: white; margin-right: 12px; float: left;
}
.comp-row {
    display: flex; align-items: center; gap: 12px;
    padding: 12px; border-radius: 8px;
    background: #F8FAFB; margin-bottom: 8px;
    border: 0.5px solid #E2E8F0;
}
.comp-badge {
    padding: 5px 14px; border-radius: 6px;
    font-size: 13px; font-weight: bold; color: white;
    min-width: 36px; text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Données ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/air_quality_clean.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df

@st.cache_data
def load_agregations():
    return pd.read_csv("data/agregation_villes.csv")

df     = load_data()
df_agg = load_agregations()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center;padding:1rem 0;'>
    <div style='width:60px;height:60px;border-radius:50%;background:#065A82;
    display:flex;align-items:center;justify-content:center;font-size:20px;
    font-weight:bold;color:white;margin:0 auto 8px;'>JR</div>
    <h3 style='color:#065A82;margin:0;'>JBALI Raja</h3>
    <p style='color:#64748b;font-size:0.8rem;margin:4px 0;'>Developpeur en IA</p>
    <p style='color:#065A82;font-weight:bold;font-size:0.75rem;'>RNCP37827BC01</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation", [
    "👋 Introduction",
    "🏠 Vue d'ensemble",
    "📥 C1 — Collecte",
    "🧹 C2/C3 — Nettoyage & Agregations",
    "🗄️ C4 — Base de donnees",
    "🔌 C5 — API FastAPI",
    "✅ Conclusion",
])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:0.8rem;color:#64748b;'>
<b>Candidat :</b> JBALI Raja<br>
<b>Formation :</b> Developpeur en IA<br>
<b>Organisme :</b> Artefact x Simplon<br>
<b>Date :</b> Avril 2026<br>
<b>Source :</b> Open-Meteo API<br>
<b>Donnees :</b> 720 mesures<br>
<b>Villes :</b> 5 villes francaises
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# INTRODUCTION
# ══════════════════════════════════════════════════════════════
if page == "👋 Introduction":
    st.markdown("""
    <div class='main-header'>
        <h1>🌿 Pipeline Qualite de l'Air</h1>
        <h3>Paris · Lyon · Marseille · Bordeaux · Lille</h3>
        <p>RNCP37827BC01 — Realiser la collecte, le stockage et la mise a disposition des donnees</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='card'>
            <div style='display:flex;align-items:center;margin-bottom:12px;'>
                <div style='width:56px;height:56px;border-radius:50%;background:#065A82;
                display:flex;align-items:center;justify-content:center;font-size:20px;
                font-weight:bold;color:white;margin-right:12px;flex-shrink:0;'>JR</div>
                <div>
                    <div style='font-size:17px;font-weight:bold;color:#1A2E3A;'>JBALI Raja</div>
                    <div style='font-size:12px;color:#64748b;'>Candidat RNCP37827BC01</div>
                </div>
            </div>
            <p><b>Formation :</b> Developpeur en Intelligence Artificielle</p>
            <p><b>Organisme :</b> Artefact x Simplon — 2024/2026</p>
            <p><b>Localisation :</b> Ile-de-France</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='card card-orange'>
            <h4>🛠️ Stack technique</h4>
            <span class='badge badge-blue'>Python</span>
            <span class='badge badge-blue'>Pandas</span>
            <span class='badge badge-purple'>PostgreSQL</span>
            <span class='badge badge-purple'>SQLAlchemy</span>
            <span class='badge badge-green'>FastAPI</span>
            <span class='badge badge-green'>Swagger</span>
            <span class='badge badge-teal'>Streamlit</span>
            <span class='badge badge-teal'>Plotly</span>
            <span class='badge badge-blue'>Git / GitHub</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card card-purple'>
            <h4>❓ Problematique</h4>
            <p>Comment collecter, stocker et exposer automatiquement
            des donnees environnementales pour les equipes data et IA ?</p>
            <br>
            <p><b>Reponse :</b> Un pipeline complet de bout en bout :</p>
            <p style='color:#065A82;font-weight:bold;'>
            API → Pandas → PostgreSQL → FastAPI → Streamlit
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='card card-green'>
            <h4>🎯 Objectif du projet</h4>
            <p>Construire un <b>pipeline de donnees complet</b> sur la
            qualite de l'air dans 5 grandes villes francaises, en utilisant
            des donnees publiques et gratuites (Open-Meteo API).</p>
            <br>
            <p>Ce projet couvre les 5 competences du bloc RNCP37827BC01 :
            collecte, preparation, agregation, stockage et mise a disposition.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🗺️ Architecture du pipeline")
    col1, col2, col3, col4, col5 = st.columns(5)
    etapes = [
        (col1, "1", "Collecte",    "Open-Meteo API", "#065A82"),
        (col2, "2", "Nettoyage",   "Pandas",         "#1C7293"),
        (col3, "3", "Agregation",  "Groupby SQL",    "#0D9488"),
        (col4, "4", "Stockage",    "PostgreSQL",     "#7C3AED"),
        (col5, "5", "API",         "FastAPI",        "#DC2626"),
    ]
    for col, num, titre, outil, color in etapes:
        col.markdown(f"""
        <div style='background:{color};color:white;padding:1rem;
        border-radius:10px;text-align:center;'>
            <div style='font-size:24px;font-weight:bold;'>{num}</div>
            <div style='font-weight:bold;font-size:14px;'>{titre}</div>
            <div style='font-size:11px;opacity:0.85;'>{outil}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════════════
elif page == "🏠 Vue d'ensemble":
    st.markdown("<div class='main-header'><h2>🏠 Vue d'ensemble</h2><p>Resultats globaux du pipeline de donnees</p></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏭 Plus polluee",  df_agg.loc[df_agg['pm25_moyen'].idxmax(), 'ville'], f"{df_agg['pm25_moyen'].max()} µg/m³")
    col2.metric("🌿 Plus saine",    df_agg.loc[df_agg['pm25_moyen'].idxmin(), 'ville'], f"{df_agg['pm25_moyen'].min()} µg/m³")
    col3.metric("📊 Total mesures", int(df_agg['nb_mesures'].sum()))
    col4.metric("🏙️ Villes",        len(df_agg))

    st.markdown("---")
    col5, col6 = st.columns(2)
    with col5:
        fig1 = px.bar(df_agg, x="ville", y="pm25_moyen", color="pm25_moyen",
                      color_continuous_scale="RdYlGn_r",
                      title="PM2.5 moyen par ville (µg/m³)")
        st.plotly_chart(fig1, use_container_width=True)
    with col6:
        fig2 = px.bar(df_agg, x="ville", y="no2_moyen", color="no2_moyen",
                      color_continuous_scale="RdYlGn_r",
                      title="NO2 moyen par ville (µg/m³)")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📊 Tableau comparatif complet")
    st.dataframe(df_agg, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# C1 COLLECTE
# ══════════════════════════════════════════════════════════════
elif page == "📥 C1 — Collecte":
    st.markdown("<div class='main-header'><h2>📥 C1 — Collecte automatisee</h2><p>API Open-Meteo — Donnees horaires — 5 villes francaises</p></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
            <h4>🔗 Source de donnees</h4>
            <p>✅ API : <b>air-quality-api.open-meteo.com</b></p>
            <p>✅ Gratuite et sans inscription</p>
            <p>✅ Polluants : PM10, PM2.5, NO2, Ozone</p>
            <p>✅ Frequence : horaire (48h collectees)</p>
            <p>✅ Gestion erreurs : timeout 10s</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card card-green'>
            <h4>📊 Resultats de la collecte</h4>
            <p>✅ <b>720 lignes</b> collectees</p>
            <p>✅ <b>5 villes</b> francaises couvvertes</p>
            <p>✅ <b>144 mesures</b> par ville</p>
            <p>✅ <b>0 valeur nulle</b></p>
            <p>✅ <b>4 polluants</b> par mesure</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📋 Script de collecte automatise")
    st.code("""
VILLES = [
    {"nom": "Paris",     "lat": 48.8566, "lon": 2.3522},
    {"nom": "Lyon",      "lat": 45.7640, "lon": 4.8357},
    {"nom": "Marseille", "lat": 43.2965, "lon": 5.3698},
    {"nom": "Bordeaux",  "lat": 44.8378, "lon": -0.5792},
    {"nom": "Lille",     "lat": 50.6292, "lon": 3.0573},
]

def collecter(lat, lon):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    r = requests.get(url, params={
        "latitude": lat, "longitude": lon,
        "hourly": "pm10,pm2_5,nitrogen_dioxide,ozone",
        "timezone": "Europe/Paris", "past_days": 1
    }, timeout=10)
    return r.json()
    """, language="python")

    st.subheader("🔍 Apercu des donnees collectees")
    ville = st.selectbox("Choisir une ville", df["ville"].unique())
    st.dataframe(
        df[df["ville"] == ville][["datetime","pm10","pm2_5","nitrogen_dioxide","ozone","indice_qualite"]].head(24),
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════
# C2/C3
# ══════════════════════════════════════════════════════════════
elif page == "🧹 C2/C3 — Nettoyage & Agregations":
    st.markdown("<div class='main-header'><h2>🧹 C2/C3 — Nettoyage & Agregations</h2><p>Preparation des donnees brutes pour exploitation analytique</p></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.success("✅ Valeurs nulles : 0")
    col2.success("✅ Doublons supprimes")
    col3.success("✅ Formats convertis")

    st.markdown("---")

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("🧹 C2 — Script de nettoyage")
        st.code("""
# 1. Conversion datetime
df["datetime"] = pd.to_datetime(df["datetime"])

# 2. Arrondi a 2 decimales
for col in ["pm10","pm2_5","nitrogen_dioxide","ozone"]:
    df[col] = df[col].round(2)

# 3. Calcul indice qualite de l'air
def indice(pm25):
    if pd.isna(pm25):   return "Inconnu"
    elif pm25 <= 10:    return "Bon"
    elif pm25 <= 25:    return "Moyen"
    elif pm25 <= 50:    return "Mauvais"
    else:               return "Tres mauvais"

df["indice_qualite"] = df["pm2_5"].apply(indice)

# 4. Suppression doublons
df = df.drop_duplicates()
        """, language="python")

    with col5:
        st.subheader("📊 C3 — Script d'agregation")
        st.code("""
# Agregation par ville
agregation_ville = df.groupby("ville").agg(
    pm10_moyen        = ("pm10",  "mean"),
    pm25_moyen        = ("pm2_5", "mean"),
    no2_moyen         = ("nitrogen_dioxide", "mean"),
    ozone_moyen       = ("ozone", "mean"),
    nb_mesures        = ("pm10",  "count")
).round(2).reset_index()

# Agregation par heure
df["heure"] = df["datetime"].dt.hour
agregation_heure = df.groupby("heure").agg(
    pm25_moyen = ("pm2_5", "mean"),
).round(2).reset_index()
        """, language="python")

    st.markdown("---")
    st.subheader("📥 Telechargement des donnees nettoyees")
    col6, col7 = st.columns(2)
    with col6:
        csv1 = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Telecharger air_quality_clean.csv (720 lignes)",
            data=csv1,
            file_name="air_quality_clean.csv",
            mime="text/csv"
        )
    with col7:
        csv2 = df_agg.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Telecharger agregation_villes.csv (5 lignes)",
            data=csv2,
            file_name="agregation_villes.csv",
            mime="text/csv"
        )

    st.markdown("---")
    col8, col9 = st.columns(2)
    with col8:
        fig_pie = px.pie(df, names="indice_qualite",
                         color_discrete_map={"Bon":"#16a34a","Moyen":"#ca8a04","Mauvais":"#dc2626"},
                         title="Repartition globale qualite de l'air")
        st.plotly_chart(fig_pie, use_container_width=True)
    with col9:
        st.subheader("Agregation par ville")
        st.dataframe(df_agg, use_container_width=True)

    st.subheader("📈 Evolution par ville")
    ville = st.selectbox("Choisir une ville", df["ville"].unique())
    df_v = df[df["ville"] == ville].copy()
    df_v["heure"] = df_v["datetime"].dt.hour

    fig3 = px.line(df_v, x="datetime", y=["pm10","pm2_5","nitrogen_dioxide","ozone"],
                   title=f"Evolution qualite air — {ville}")
    st.plotly_chart(fig3, use_container_width=True)

    agg_h = df_v.groupby("heure")["pm2_5"].mean().reset_index()
    fig4 = px.bar(agg_h, x="heure", y="pm2_5",
                  title=f"Pollution PM2.5 par heure — {ville}",
                  color="pm2_5", color_continuous_scale="RdYlGn_r")
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# C4
# ══════════════════════════════════════════════════════════════
elif page == "🗄️ C4 — Base de donnees":
    st.markdown("<div class='main-header'><h2>🗄️ C4 — Base de donnees PostgreSQL</h2><p>Choix SQL justifie — 3 tables — ORM SQLAlchemy</p></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card card-purple'>
            <h4>🤔 Pourquoi PostgreSQL ?</h4>
            <p>✅ Donnees structurees et relationnelles</p>
            <p>✅ Requetes SQL complexes (GROUP BY, JOIN)</p>
            <p>✅ Garanties ACID pour l'integrite</p>
            <p>✅ Integration SQLAlchemy ORM Python</p>
            <p>✅ Meilleur choix vs MongoDB pour ce projet</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card card-green'>
            <h4>📊 Resultats</h4>
            <p>✅ <b>3 tables</b> creees</p>
            <p>✅ <b>5 villes</b> inserees</p>
            <p>✅ <b>720 mesures</b> inserees</p>
            <p>✅ <b>5 agregations</b> inserees</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📐 Schema MCD / MLD")
    st.code("""
Table villes          Table mesures              Table agregations
─────────────         ──────────────────         ─────────────────
id (PK)               id (PK)                    id (PK)
nom                   ville                      ville
latitude              datetime                   pm10_moyen
longitude             pm10                       pm25_moyen
                      pm2_5                      no2_moyen
                      nitrogen_dioxide           ozone_moyen
                      ozone                      nb_mesures
                      indice_qualite
                      collecte_le
    """)

    st.subheader("📋 Donnees en base")
    tab1, tab2 = st.tabs(["📊 Mesures (50 premieres)", "📈 Agregations"])
    with tab1:
        st.dataframe(df.head(50), use_container_width=True)
    with tab2:
        st.dataframe(df_agg, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# C5
# ══════════════════════════════════════════════════════════════
elif page == "🔌 C5 — API FastAPI":
    st.markdown("<div class='main-header'><h2>🔌 C5 — API FastAPI securisee</h2><p>Documentation Swagger auto — Securisation par cle API</p></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card'>
            <h4>⚡ FastAPI + Swagger</h4>
            <p>✅ Documentation auto OpenAPI 3.1</p>
            <p>✅ Securisation par cle API</p>
            <p>✅ 5 endpoints disponibles</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card card-red'>
            <h4>🔐 Securisation</h4>
            <p>• Header requis : <code>X-API-Key</code></p>
            <p>• Sans cle → <b>403 Forbidden</b></p>
            <p>• Avec cle → <b>donnees JSON ✅</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📖 Documentation Swagger")
    st.markdown("""
    <div class='card card-teal'>
        <h4>🔗 Lien Swagger UI</h4>
        <p>La documentation interactive est disponible sur :</p>
        <a href='http://127.0.0.1:8000/docs' target='_blank'
        style='display:inline-block;background:#065A82;color:white;
        padding:10px 20px;border-radius:8px;text-decoration:none;
        font-weight:bold;margin-top:8px;'>
            Ouvrir Swagger UI → http://127.0.0.1:8000/docs
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📡 Endpoints disponibles")
    st.table(pd.DataFrame([
        ["GET", "/",               "Statut de l'API",       "Non", "200 OK"],
        ["GET", "/villes",         "Liste des 5 villes",    "Oui", "200 OK"],
        ["GET", "/mesures/{ville}","Mesures par ville",     "Oui", "200 OK"],
        ["GET", "/agregations",    "Moyennes par ville",    "Oui", "200 OK"],
        ["GET", "/stats",          "Statistiques globales", "Oui", "200 OK"],
    ], columns=["Methode", "Endpoint", "Description", "Auth", "Status"]))

    st.subheader("🧪 Exemple de test")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Avec cle API — 200 OK ✅**")
        st.code("""
curl -X GET "http://127.0.0.1:8000/villes" \\
  -H "X-API-Key: monsecretkey2024"
        """, language="bash")
    with col4:
        st.markdown("**Sans cle — 403 Forbidden ❌**")
        st.code("""
curl -X GET "http://127.0.0.1:8000/villes"

→ {"detail": "Not authenticated"}
        """, language="bash")

    st.subheader("📊 Reponse JSON exemple")
    st.code("""
[
  {"id":1,"nom":"Paris","latitude":48.8566,"longitude":2.3522},
  {"id":2,"nom":"Lyon","latitude":45.764,"longitude":4.8357},
  {"id":3,"nom":"Marseille","latitude":43.2965,"longitude":5.3698},
  {"id":4,"nom":"Bordeaux","latitude":44.8378,"longitude":-0.5792},
  {"id":5,"nom":"Lille","latitude":50.6292,"longitude":3.0573}
]
    """, language="json")

# ══════════════════════════════════════════════════════════════
# CONCLUSION
# ══════════════════════════════════════════════════════════════
elif page == "✅ Conclusion":
    st.markdown("<div class='main-header'><h2>✅ Conclusion</h2><p>Bilan du projet et perspectives d'evolution</p></div>", unsafe_allow_html=True)

    st.subheader("🏆 Bilan des competences — RNCP37827BC01")

    competences = [
        ("C1", "Collecte automatisee",    "720 lignes collectees — Open-Meteo API — gestion erreurs timeout",    "#065A82"),
        ("C2", "Preparation des donnees", "Nettoyage Pandas — conversion types — indice qualite — 0 nulls",     "#1C7293"),
        ("C3", "Agregation de donnees",   "Agregations par ville et par heure — insights metier detectes",      "#0D9488"),
        ("C4", "Creation base de donnees","PostgreSQL — 3 tables MCD/MLD — SQLAlchemy ORM — 720 inserees",      "#7C3AED"),
        ("C5", "Mise a disposition API",  "FastAPI — Swagger OpenAPI — securisation par cle — 5 endpoints",    "#DC2626"),
    ]

    for code, titre, detail, color in competences:
        st.markdown(f"""
        <div class='comp-row'>
            <div class='comp-badge' style='background:{color};'>{code}</div>
            <div>
                <div style='font-size:14px;font-weight:bold;color:#1A2E3A;'>{titre}</div>
                <div style='font-size:12px;color:#64748b;'>{detail}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card card-green'>
            <h4>💡 Ce que j'ai appris</h4>
            <p>✅ Cycle complet d'un projet data</p>
            <p>✅ Architecture pipeline de bout en bout</p>
            <p>✅ Modelisation BDD relationnelle (MCD/MLD)</p>
            <p>✅ Developpement API REST securisee</p>
            <p>✅ Visualisation interactive avec Streamlit</p>
            <p>✅ Utilisation de donnees publiques reelles</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card card-purple'>
            <h4>🚀 Perspectives d'evolution</h4>
            <p>🌐 Deploiement cloud (Render / Railway)</p>
            <p>🤖 Modele ML pour prediction qualite air</p>
            <p>⏰ Automatisation Airflow (collecte horaire)</p>
            <p>🔔 Alertes si seuils OMS depasses</p>
            <p>🗺️ Carte interactive France avec Folium</p>
            <p>📈 Extension a 30+ villes francaises</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='background:#065A82;padding:2rem;border-radius:12px;
    text-align:center;color:white;'>
        <h2>Merci pour votre attention</h2>
        <p style='font-size:1.1rem;'>
        Pipeline complet : Collecte → Nettoyage → Agregation → PostgreSQL → FastAPI → Streamlit
        </p>
        <p><b>JBALI Raja — Developpeur en Intelligence Artificielle — Artefact x Simplon — 2026</b></p>
    </div>
    """, unsafe_allow_html=True)