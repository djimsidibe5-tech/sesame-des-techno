from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# 1. Montage du dossier static pour les fichiers CSS et images
# Assurez-vous que le dossier 'static' existe bien à la racine
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Configuration du dossier des templates HTML
# Assurez-vous que le dossier 'templates' existe bien à la racine
templates = Jinja2Templates(directory="templates")

# 3. Données académiques (exemple de structure)
ACADEMIC_DATA = {
    "Licence 1": ["Mécanique du point", "Optique géométrique", "Thermodynamique"],
    "Licence 2": ["Électromagnétisme", "Ondes mécaniques", "Analyse numérique"],
    "Licence 3": ["Physique atomique", "Physique du solide", "Mécanique quantique"],
    "Master 1": ["Physique théorique", "Traitement du signal", "Méthodes numériques"],
    "Master 2": ["Énergie", "Recherche bibliographique", "Thèse"]
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Envoie le fichier index.html avec les données
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": ACADEMIC_DATA
    })
