
from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os, pandas as pd

load_dotenv()

app = FastAPI(
    title="🌿 Air Quality API",
    description="API de qualité de l air des villes françaises",
    version="1.0.0"
)

# Sécurisation par clé API
API_KEY        = os.getenv("API_KEY", "monsecretkey2024")
api_key_header = APIKeyHeader(name="X-API-Key")

def verifier_cle(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Clé API invalide")
    return key

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DATABASE_URL)

@app.get("/", tags=["Info"])
def accueil():
    return {"message": "🌿 Air Quality API", "version": "1.0.0", "status": "ok"}

@app.get("/villes", tags=["Villes"])
def get_villes(api_key: str = Security(verifier_cle)):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM villes"))
        return [dict(row._mapping) for row in result]

@app.get("/mesures/{ville}", tags=["Mesures"])
def get_mesures(ville: str, limit: int = 24, api_key: str = Security(verifier_cle)):
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT * FROM mesures WHERE ville = :ville ORDER BY datetime DESC LIMIT :limit"
        ), {"ville": ville, "limit": limit})
        rows = [dict(row._mapping) for row in result]
        if not rows:
            raise HTTPException(status_code=404, detail=f"Ville {ville} non trouvée")
        return rows

@app.get("/agregations", tags=["Agrégations"])
def get_agregations(api_key: str = Security(verifier_cle)):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM agregations ORDER BY pm25_moyen DESC"))
        return [dict(row._mapping) for row in result]

@app.get("/stats", tags=["Stats"])
def get_stats(api_key: str = Security(verifier_cle)):
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM mesures")).scalar()
        villes = conn.execute(text("SELECT COUNT(DISTINCT ville) FROM mesures")).scalar()
        return {"total_mesures": total, "nb_villes": villes}
