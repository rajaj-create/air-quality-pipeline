import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

st.set_page_config(page_title="🌿 Air Quality Pipeline", layout="wide")

API_URL = "http://127.0.0.1:8000"
API_KEY = "monsecretkey2024"
headers = {"X-API-Key": API_KEY}

# ── Sidebar navigation ────────────────────────
st.sidebar.title("🌿 Air Quality Pipeline")
st.sidebar.markdown("**RNCP37827BC01**")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "🏠 Vue d'ensemble",
    "📥 C1 — Collecte",
    "🧹 C2/C3 — Nettoyage & Agrégations",
    "🗄️ C4 — Base de données",
    "🔌 C5 — API"
])

# ── Charger données ───────────────────────────
@st.cache_data
def load_agregations():
    return pd.DataFrame(requests.get(f"{API_URL}/agregations", headers=headers).json())

@st.cache_data
def load_villes():
    return pd.DataFrame(requests.get(f"{API_URL}/villes", headers=headers).json())

@st.cache_data
def load_mesures(ville):
    return pd.DataFrame(requests.get(f"{API_URL}/mesures/{ville}?limit=48", headers=headers).json())

df_agg   = load_agregations()
df_villes = load_villes()

# ══════════════════════════════════════════════
if page == "🏠 Vue d'ensemble":
    st.title("🌿 Dashboard Qualité de l'Air — France")
    st.markdown("Pipeline de données complet : collecte → nettoyage → stockage → API")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏭 Ville la plus polluée", df_agg.loc[df_agg['pm25_moyen'].idxmax(), 'ville'], f"{df_agg['pm25_moyen'].max()} µg/m³")
    col2.metric("🌿 Ville la plus saine",   df_agg.loc[df_agg['pm25_moyen'].idxmin(), 'ville'], f"{df_agg['pm25_moyen'].min()} µg/m³")
    col3.metric("📊 Total mesures",         int(df_agg['nb_mesures'].sum()))
    col4.metric("🏙️ Villes analysées",      len(df_agg))

    st.markdown("---")
    col5, col6 = st.columns(2)

    with col5:
        fig1 = px.bar(df_agg, x="ville", y="pm25_moyen", color="pm25_moyen",
                      color_continuous_scale="RdYlGn_r", title="🔴 PM2.5 moyen par ville (µg/m³)")
        st.plotly_chart(fig1)

    with col6:
        fig2 = px.bar(df_agg, x="ville", y="no2_moyen", color="no2_moyen",
                      color_continuous_scale="RdYlGn_r", title="🟡 NO2 moyen par ville (µg/m³)")
        st.plotly_chart(fig2)

    st.markdown("---")
    st.subheader("📊 Tableau comparatif")
    st.dataframe(df_agg, use_container_width=True)

# ══════════════════════════════════════════════
elif page == "📥 C1 — Collecte":
    st.title("📥 C1 — Collecte automatisée")
    st.markdown("---")

    st.success("✅ Source : **Open-Meteo Air Quality API** (gratuite, sans inscription)")

    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **🔗 API utilisée**
        - URL : `air-quality-api.open-meteo.com`
        - Paramètres : PM10, PM2.5, NO2, Ozone
        - Fréquence : horaire
        - Couverture : dernières 48h
        """)
    with col2:
        st.info("""
        **🏙️ Villes collectées**
        - Paris, Lyon, Marseille
        - Bordeaux, Lille
        - 144 mesures/ville
        - Total : 720 lignes
        """)

    st.markdown("---")
    st.subheader("📋 Script de collecte")
    st.code("""
def collecter(lat, lon):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    r = requests.get(url, params={
        "latitude": lat, "longitude": lon,
        "hourly": "pm10,pm2_5,nitrogen_dioxide,ozone",
        "timezone": "Europe/Paris", "past_days": 1
    }, timeout=10)
    return r.json()
    """, language="python")

    st.subheader("📊 Données collectées")
    ville = st.selectbox("Voir les données d'une ville", df_villes["nom"].tolist())
    df_m = load_mesures(ville)
    df_m["datetime"] = pd.to_datetime(df_m["datetime"])
    st.dataframe(df_m[["datetime","pm10","pm2_5","nitrogen_dioxide","ozone"]].head(24))

# ══════════════════════════════════════════════
elif page == "🧹 C2/C3 — Nettoyage & Agrégations":
    st.title("🧹 C2/C3 — Nettoyage & Agrégations")
    st.markdown("---")

    st.subheader("C2 — Nettoyage des données")
    col1, col2, col3 = st.columns(3)
    col1.success("✅ Valeurs nulles : **0**")
    col2.success("✅ Doublons supprimés")
    col3.success("✅ Formats convertis")

    st.code("""
# Conversion datetime
df["datetime"] = pd.to_datetime(df["datetime"])

# Arrondi à 2 décimales
for col in ["pm10","pm2_5","nitrogen_dioxide","ozone"]:
    df[col] = df[col].round(2)

# Indice qualité
def indice(pm25):
    if pm25 <= 10:  return "Bon"
    elif pm25 <= 25: return "Moyen"
    elif pm25 <= 50: return "Mauvais"
    else:            return "Très mauvais"
    """, language="python")

    st.markdown("---")
    st.subheader("C3 — Règles d'agrégation")

    ville = st.selectbox("Choisir une ville", df_villes["nom"].tolist())
    df_m = load_mesures(ville)
    df_m["datetime"] = pd.to_datetime(df_m["datetime"])
    df_m["heure"]    = df_m["datetime"].dt.hour

    col4, col5 = st.columns(2)
    with col4:
        fig3 = px.line(df_m, x="datetime", y=["pm10","pm2_5"],
                       title=f"Évolution PM — {ville}")
        st.plotly_chart(fig3)
    with col5:
        agg_h = df_m.groupby("heure")["pm2_5"].mean().reset_index()
        fig4  = px.bar(agg_h, x="heure", y="pm2_5",
                       title="Pollution PM2.5 par heure de la journée",
                       color="pm2_5", color_continuous_scale="RdYlGn_r")
        st.plotly_chart(fig4)

# ══════════════════════════════════════════════
elif page == "🗄️ C4 — Base de données":
    st.title("🗄️ C4 — Base de données PostgreSQL")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **✅ Choix technologique : PostgreSQL**
        - Données structurées et relationnelles
        - Requêtes SQL complexes
        - Fiabilité et performance
        - ORM SQLAlchemy (Python)
        """)
    with col2:
        st.info("""
        **📊 3 tables créées**
        - `villes` : 5 villes françaises
        - `mesures` : 720 mesures horaires
        - `agregations` : moyennes par ville
        """)

    st.markdown("---")
    st.subheader("📐 Schéma MCD")
    st.code("""
Table villes          Table mesures              Table agregations
─────────────         ──────────────────         ─────────────────
id (PK)               id (PK)                    id (PK)
nom                   ville (FK)                 ville
latitude              datetime                   pm10_moyen
longitude             pm10                       pm25_moyen
                      pm2_5                      no2_moyen
                      nitrogen_dioxide           ozone_moyen
                      ozone                      nb_mesures
                      indice_qualite
                      collecte_le
    """)

    st.subheader("📋 Données en base")
    tab1, tab2 = st.tabs(["Villes", "Agrégations"])
    with tab1:
        st.dataframe(df_villes)
    with tab2:
        st.dataframe(df_agg)

# ══════════════════════════════════════════════
elif page == "🔌 C5 — API":
    st.title("🔌 C5 — API FastAPI sécurisée")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **✅ FastAPI + Swagger**
        - Documentation auto OpenAPI
        - Sécurisation par clé API
        - 4 endpoints disponibles
        """)
    with col2:
        st.info("""
        **🔐 Sécurisation**
        - Header : `X-API-Key`
        - Sans clé → 403 Forbidden
        - Avec clé → données JSON
        """)

    st.markdown("---")
    st.subheader("📡 Tester l'API en direct")

    endpoint = st.selectbox("Choisir un endpoint", [
        "GET /",
        "GET /villes",
        "GET /agregations",
        "GET /stats"
    ])

    if st.button("🚀 Tester"):
        url_map = {
            "GET /":            f"{API_URL}/",
            "GET /villes":      f"{API_URL}/villes",
            "GET /agregations": f"{API_URL}/agregations",
            "GET /stats":       f"{API_URL}/stats"
        }
        response = requests.get(url_map[endpoint], headers=headers)
        st.code(response.json(), language="json")
        st.success(f"✅ Status : {response.status_code}")

    st.markdown("---")
    st.subheader("📖 Documentation Swagger")
    st.markdown("👉 [Ouvrir Swagger UI](http://127.0.0.1:8000/docs)")