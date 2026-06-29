main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montage des fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration des templates
templates = Jinja2Templates(directory="templates")

# Structure de vos données académiques
ACADEMIC_DATA = {
    "Licence 1": ["Mécanique du point", "Optique géométrique", "Thermodynamique", "Algèbre linéaire"],
    "Licence 2": ["Électromagnétisme", "Ondes mécaniques", "Analyse numérique", "Physique statistique"],
    "Licence 3": ["Physique atomique", "Physique du solide", "Mécanique analytique", "Relativité"],
    "Master 1": ["Physique théorique", "Traitement du signal", "Méthodes numériques"],
    "Master 2": ["Énergie", "Recherche bibliographique", "Thèse"]
}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": ACADEMIC_DATA
    })

# Commande pour lancer : uvicorn main:app --reload
