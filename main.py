from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

app = FastAPI(title="Horizon - Sésame des Techno")

# Configuration des dossiers
dossier_fichiers = Path("fichiers")
dossier_fichiers.mkdir(exist_ok=True)
categories = ["Algèbre Linéaire", "Informatique", "Physique"] # Adapté à l'image

for cat in categories:
    (dossier_fichiers / cat).mkdir(exist_ok=True)

app.mount("/fichiers", StaticFiles(directory="fichiers"), name="fichiers")

@app.get("/", response_class=HTMLResponse)
async def home():
    # Construction des sections
    sections_html = ""
    for cat in categories:
        chemin_cat = dossier_fichiers / cat
        fichiers = [f.name for f in chemin_cat.iterdir() if f.is_file()]
        docs = "".join([f'<div class="doc-item">📄 {f} <a href="/fichiers/{cat}/{f}" class="btn-dl">⬇ PDF</a></div>' for f in fichiers])
        
        sections_html += f"""
        <div class="category-box">
            <h3>{cat}</h3>
            {docs if docs else '<p style="color:#aaa;">Aucun sujet disponible.</p>'}
        </div>"""

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            :root {{ --bleu: #1e3a8a; --or: #fbbf24; --vert: #059669; --creme: #fdfaf6; }}
            body {{ background-color: var(--creme); font-family: 'Segoe UI', sans-serif; color: var(--bleu); padding: 40px; display: flex; flex-direction: column; align-items: center; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .container {{ width: 100%; max-width: 800px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .category-box {{ background: white; padding: 20px; border-radius: 15px; border: 2px solid var(--or); box-shadow: 5px 5px 0px var(--bleu); }}
            .doc-item {{ display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; margin-top: 5px; }}
            .btn-dl {{ background: var(--vert); color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 12px; }}
            .upload-form {{ grid-column: span 2; background: var(--bleu); color: white; padding: 20px; border-radius: 15px; }}
            button {{ background: var(--or); border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>HORIZON - SÉSAME DES TECHNO</h1>
            <p>API de centralisation des anciens sujets d'examens (v1.0.0)</p>
        </div>
        
        <div class="container">
            <div class="upload-form">
                <h2>➕ Ajouter un nouveau sujet</h2>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <select name="categorie" style="padding:10px;">
                        {''.join([f'<option value="{c}">{c}</option>' for c in categories])}
                    </select>
                    <input type="file" name="file" required>
                    <button type="submit">POSTER LE SUJET</button>
                </form>
            </div>
            {sections_html}
        </div>
    </body>
    </html>
    """

@app.post("/upload")
async def upload(categorie: str = Form(...), file: UploadFile = File(...)):
    file_path = dossier_fichiers / categorie / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse(url="/", status_code=303)
