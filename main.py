from fastapi import FastAPI, UploadFile, HTTPException
from fastapi import File, Form  # Importation corrigée et sécurisée
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI(title="Sésame des Techno")

# Initialisation propre du dossier de stockage sur le disque Render
dossier_fichiers = Path("fichiers")
dossier_fichiers.mkdir(exist_ok=True)

categories = [
    "Algèbre Linéaire",
    "Analyse & Calcul Numérique",
    "Probabilités & Statistiques",
    "Thermodynamique",
    "Électromagnétisme",
    "Optique & Physique Ondulatoire",
    "Mécanique du Point & Fluides",
    "Chimie Organique",
    "Chimie Générale & Solutions",
    "Informatique (Python & SQL)",
    "Bureautique (Excel, Access, Word)",
    "Sujets de Concours"
]

# Création des sous-dossiers au démarrage
for cat in categories:
    (dossier_fichiers / cat).mkdir(exist_ok=True)

# Montage sécurisé des fichiers statiques
app.mount("/fichiers", StaticFiles(directory="fichiers"), name="fichiers")

@app.get("/", response_class=HTMLResponse)
async def home():
    options_select = ""
    blocs_matieres_html = ""

    # Génération ultra-légère des composants HTML
    for cat in categories:
        options_select += f'<option value="{cat}">{cat}</option>'
       
        chemin_cat = dossier_fichiers / cat
        # Utilisation de os.scandir (très économe en RAM) au lieu de iterdir()
        fichiers = []
        if chemin_cat.exists():
            with os.scandir(chemin_cat) as entries:
                for entry in entries:
                    if entry.is_file() and not entry.name.startswith('.'):
                        fichiers.append(entry.name)

        liste_fichiers_html = ""
        if not fichiers:
            liste_fichiers_html = "<p class='no-file'>Aucun sujet disponible.</p>"
        else:
            liste_fichiers_html = "<ul class='file-list'>"
            for sujet in fichiers:
                liste_fichiers_html += f"""
                <li class='file-item'>
                    <span class='file-name'>📄 {sujet}</span>
                    <a href='/fichiers/{cat}/{sujet}' download class='btn-download'>Télécharger</a>
                </li>"""
            liste_fichiers_html += "</ul>"

        classe_carte = "card-cat special" if cat == "Sujets de Concours" else "card-cat"
        blocs_matieres_html += f"""
        <div class='{classe_carte}'>
            <h3>{cat}</h3>
            {liste_fichiers_html}
        </div>"""

    html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sésame des Techno</title>
    <style>
        body { margin: 0; font-family: sans-serif; background-color: #0f172a; color: #f8fafc; padding: 20px; }
        .container { max-width: 1200px; margin: auto; background: #1e293b; padding: 25px; border-radius: 12px; }
        h1 { color: #38bdf8; text-align: center; }
        .upload-section { background: #1e3a8a; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
        .upload-form { display: flex; gap: 12px; flex-wrap: wrap; }
        select, input[type="file"] { background: #0f172a; padding: 10px; border-radius: 6px; border: 1px solid #475569; color: white; }
        .btn-submit { background: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; }
        .grid-categories { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card-cat { background: #0f172a; padding: 15px; border-radius: 8px; border-top: 3px solid #38bdf8; }
        .card-cat.special { border-top-color: #f59e0b; }
        .file-list { list-style: none; padding: 0; }
        .file-item { background: rgba(255,255,255,0.05); margin: 5px 0; padding: 8px; border-radius: 4px; display: flex; justify-content: space-between; }
        .btn-download { background: #2563eb; color: white; text-decoration: none; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sésame des Techno 🎓</h1>
        <div class="upload-section">
            <form action="/upload-sujet/" method="post" enctype="multipart/form-data" class="upload-form">
                <select name="categorie" required>
                    <option value="" disabled selected>Choisir la matière...</option>
                    </select>
                <input type="file" name="file" required>
                <button type="submit" class="btn-submit">Mettre en ligne</button>
            </form>
        </div>
        <div class="grid-categories">
            </div>
    </div>
</body>
</html>"""

    html_content = html_content.replace("", options_select)
    html_content = html_content.replace("", blocs_matieres_html)
    return HTMLResponse(content=html_content)

@app.post("/upload-sujet/")
async def uploader_sujet(categorie: str = Form(...), file: UploadFile = File(...)):
    if categorie not in categories:
        raise HTTPException(status_code=400, detail="Matière invalide")
   
    chemin_destination = dossier_fichiers / categorie / file.filename
    with chemin_destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
       
    return HTMLResponse(content="""
    <script>
        alert("Fichier mis en ligne avec succès !");
        window.location.href = "/";
    </script>
    """)
