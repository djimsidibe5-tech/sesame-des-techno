from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

app = FastAPI(title="Sésame des Techno")

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

for cat in categories:
    (dossier_fichiers / cat).mkdir(exist_ok=True)

app.mount("/fichiers", StaticFiles(directory="fichiers"), name="fichiers")

@app.get("/", response_class=HTMLResponse)
async def home():
    options_select = "".join(
        f'<option value="{cat}">{cat}</option>' for cat in categories
    )

    blocs = []
    for cat in categories:
        chemin_cat = dossier_fichiers / cat
        fichiers = []
        if chemin_cat.exists():
            with os.scandir(chemin_cat) as entries:
                fichiers = [e.name for e in entries if e.is_file() and not e.name.startswith('.')]

        if fichiers:
            items = "".join(
                f"<li class='file-item'>"
                f"<span>📄 {s}</span>"
                f"<a href='/fichiers/{cat}/{s}' download class='btn-download'>Télécharger</a>"
                f"</li>"
                for s in fichiers
            )
            liste_html = f"<ul class='file-list'>{items}</ul>"
        else:
            liste_html = "<p class='no-file'>Aucun sujet disponible.</p>"

        classe = "card-cat special" if cat == "Sujets de Concours" else "card-cat"
        blocs.append(f"<div class='{classe}'><h3>{cat}</h3>{liste_html}</div>")

    blocs_html = "".join(blocs)

    # HTML retourné directement (pas de double replace)
    return HTMLResponse(content=f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sésame des Techno</title>
    <style>
        body {{ margin:0; font-family:sans-serif; background:#0f172a; color:#f8fafc; padding:20px; }}
        .container {{ max-width:1200px; margin:auto; background:#1e293b; padding:25px; border-radius:12px; }}
        h1 {{ color:#38bdf8; text-align:center; }}
        .upload-section {{ background:#1e3a8a; padding:20px; border-radius:8px; margin-bottom:30px; }}
        .upload-form {{ display:flex; gap:12px; flex-wrap:wrap; }}
        select, input[type="file"] {{ background:#0f172a; padding:10px; border-radius:6px; border:1px solid #475569; color:white; }}
        .btn-submit {{ background:#10b981; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer; }}
        .grid-categories {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; }}
        .card-cat {{ background:#0f172a; padding:15px; border-radius:8px; border-top:3px solid #38bdf8; }}
        .card-cat.special {{ border-top-color:#f59e0b; }}
        .file-list {{ list-style:none; padding:0; }}
        .file-item {{ background:rgba(255,255,255,0.05); margin:5px 0; padding:8px; border-radius:4px; display:flex; justify-content:space-between; }}
        .btn-download {{ background:#2563eb; color:white; text-decoration:none; padding:2px 8px; border-radius:4px; font-size:12px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>Sésame des Techno 🎓</h1>
    <div class="upload-section">
        <form action="/upload-sujet/" method="post" enctype="multipart/form-data" class="upload-form">
            <select name="categorie" required>
                <option value="" disabled selected>Choisir la matière...</option>
                {options_select}
            </select>
            <input type="file" name="file" required>
            <button type="submit" class="btn-submit">Mettre en ligne</button>
        </form>
    </div>
    <div class="grid-categories">{blocs_html}</div>
</div>
</body>
</html>""")


@app.post("/upload-sujet/")
async def uploader_sujet(categorie: str = Form(...), file: UploadFile = File(...)):
    if categorie not in categories:
        raise HTTPException(status_code=400, detail="Matière invalide")

    chemin_destination = dossier_fichiers / categorie / file.filename

    # ✅ Lecture par chunks de 64KB (économie mémoire)
    with chemin_destination.open("wb") as buffer:
        while chunk := await file.read(65536):  # 64KB à la fois
            buffer.write(chunk)

    return HTMLResponse(content="""
    <script>
        alert("Fichier mis en ligne avec succès !");
        window.location.href = "/";
    </script>
    """)
