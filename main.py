from typing import List, Optional, Any, Dict
from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Field

# --- MODÈLES DE DONNÉES ---
class SujetBase(BaseModel):
    matiere: str
    annee: int
    semestre: int
    type_session: str
    url_sujet: str
    url_correction: Optional[str] = None

class SujetCreate(SujetBase):
    pass

class Sujet(SujetBase):
    id: int

# --- BASE DE DONNÉES TEMPORAIRE ---
FAKE_SUJETS_DB: List[Dict[str, Any]] = [
    {
        "id": 1,
        "matiere": "Thermodynamique",
        "annee": 2025,
        "semestre": 1,
        "type_session": "Principale",
        "url_sujet": "https://horizon-storage.ci/sujets/thermo_2025.pdf",
        "url_correction": "https://horizon-storage.ci/corrections/cor_thermo_2025.pdf" },
    {
        "id": 2,
        "matiere": "Algèbre Linéaire",
        "annee": 2024,
        "semestre": 1,
        "type_session": "Rattrapage",
        "url_sujet": "https://horizon-storage.ci/sujets/algebre_2024.pdf",
        "url_correction": None
    }
]

# --- APPLICATION ---
from fastapi import FastAPI,HTMLResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
app = FastAPI(
    title="Horizon - Sésame des Techno",
    version="1.0.0",
    description="API de centralisation des anciens sujets d'examens et corrections")
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()
@app.get("/", response_class=HTMLResponse)
async def home():
    return 
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sésame des Techno - Horizon</title>

    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: # 0f172a;
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100 vh;
            text-align: center; }
         container {
            max-width: 800px;
            padding: 20px;}
        h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;}
        p {
            font-size: 1.2rem;
            color: #94a3b8;
            margin-bottom: 30px;}
        .btn {
            display: inline-block;
            background: #2563eb;
            color: white;
            text-decoration: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-weight: bold;
            transition: background 0.3s;
            font-size: 1.1rem;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4); }
        .btn:hover {
            background: #1d4ed8; }
        .preview-img {
            margin-top: 40px;
            max-width: 90%;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
</head>

<body>
    <div class="container">
        <h1>Sésame des Techno</h1>
        <p>
            Votre plateforme de centralisation des anciens sujets
            d'examens et corrections.
        </p>
        <a href="/docs" class="btn">
            Accéder aux Sujets & API
        </a>
        <br><br>
        <img
            src="http://googleusercontent.com/generated_image_content/0"
            alt="Horizon Interface"
            class="preview-img"
        >
    </div>
</body>
</html>
# --- CONFIGURATION DES FICHIERS STATIQUES ---

# Définition du répertoire cible
dossier_fichiers = Path("fichiers")

# Création du dossier s'il n'existe pas (exist_ok=True évite l'erreur si le dossier existe déjà)
dossier_fichiers.mkdir(parents=True, exist_ok=True)

# Montage du dossier pour rendre les fichiers accessibles via l'URL /telecharger
app.mount(
    "/telecharger", 
    StaticFiles(directory=dossier_fichiers), 
    name="telechargements"
)


# --- ROUTES ---

@app.get("/sujets", tags=["Sujets & Corrections"], summary="Récupérer les sujets disponibles")
def list_sujets(
    matiere: Optional[str] = Query(None, description="Filtrer par nom de matière"),
    annee: Optional[int] = Query(None, description="Filtrer par année universitaire")
):
    resultats = FAKE_SUJETS_DB
    
    if matiere:
        resultats = [s for s in resultats if matiere.lower() in s["matiere"].lower()]
    if annee:
        resultats = [s for s in resultats if s["annee"] == annee]
        
    return resultats

@app.post("/sujets", tags=["Sujets & Corrections"], status_code=status.HTTP_201_CREATED, summary="Ajouter un nouveau sujet")
def create_sujet(sujet: SujetCreate):
    new_id = max((s["id"] for s in FAKE_SUJETS_DB), default=0) + 1
    new_sujet = sujet.model_dump()
    new_sujet["id"] = new_id
    
    FAKE_SUJETS_DB.append(new_sujet)
    return new_sujet

@app.put("/sujets/{sujet_id}/correction", tags=["Sujets & Corrections"], summary="Ajouter/Mettre à jour la correction")
def update_correction(sujet_id: int, url_correction: str = Query(..., description="URL du fichier de correction")):
    for sujet in FAKE_SUJETS_DB:
        if sujet["id"] == sujet_id:
            sujet["url_correction"] = url_correction
            return {"message": "Correction mise à jour avec succès", "sujet": sujet}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Sujet introuvable"
    )
