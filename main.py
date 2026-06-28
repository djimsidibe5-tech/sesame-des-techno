from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

app = FastAPI(
    title="Horizon - Sésame des Techno",
    version="1.1.0",
    description="API de centralisation des anciens sujets d'examens et corrections"
)

# Configuration du dossier de stockage
dossier_fichiers = Path("fichiers")
dossier_fichiers.mkdir(exist_ok=True)

# Montage des fichiers statiques
app.mount("/fichiers", StaticFiles(directory="fichiers"), name="fichiers")

def generer_html_liste():
    sujets = [f.name for f in dossier_fichiers.iterdir() if f.is_file()]
    if not sujets:
        return '<p style="color: #bbb; font-style: italic;">Aucun sujet disponible pour le moment.</p>'
    
    html = '<ul style="list-style: none; padding: 0; text-align: left; max-width: 500px; margin: 0 auto;">'
    for sujet in sujets:
        html += f"""
        <li style="background: rgba(255,255,255,0.05); margin: 8px 0; padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
            <span>📄 {sujet}</span>
            <a href="/fichiers/{sujet}" style="background: #2563eb; color: white; text-decoration: none; padding: 6px 12px; border-radius: 4px; font-size: 14px; transition: 0.2s;" onmouseover="this.style.background='#1d4ed8'" onmouseout="this.style.background='#2563eb'">Télécharger</a>
        </li>"""
    html += "</ul>"
    return html

@app.get("/", response_class=HTMLResponse)
async def home():
    liste_html = generer_html_liste()
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sésame des Techno - Horizon</title>
    <style>
        body {{ margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: white; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 20px; box-sizing: border-box; }}
        .container {{ max-width: 800px; width: 100%; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); text-align: center; }}
        h1 {{ color: #38bdf8; margin-bottom: 10px; }}
        .subtitle {{ color: #94a3b8; margin-bottom: 30px; }}
        .section {{ background: #0f172a; padding: 20px; border-radius: 8px; margin-bottom: 25px; }}
        h2 {{ font-size: 18px; color: #38bdf8; margin: 0 0 15px 0; text-align: left; border-bottom: 1px solid #334155; padding-bottom: 8px; }}
        input[type="file"] {{ background: #1e293b; padding: 8px; border-radius: 6px; border: 1px dashed #475569; color: #cbd5e1; cursor: pointer; }}
        button {{ background: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }}
        button:hover {{ background: #059669; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Sésame des Techno 🎓</h1>
        <p class="subtitle">Espace collaboratif de centralisation des anciens sujets et corrections</p>
        <div class="section">
            <h2>Ajouter un nouveau sujet</h2>
            <form action="/upload-sujet" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit">Téléverser sur le site</button>
            </form>
        </div>
        <div class="section">
            <h2>Sujets et Corrections disponibles</h2>
            {liste_html}
        </div>
    </div>
</body>
</html>"""

@app.post("/upload-sujet")
async def uploader_sujet(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier invalide")
    
    file_path = dossier_fichiers / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return RedirectResponse(url="/", status_code=303)
