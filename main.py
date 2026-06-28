from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

app = FastAPI(
    title="Horizon - Sésame des Techno",
    version="1.4.0",
    description="Plateforme de centralisation complète des ressources Sciences & Technologies"
)

# Configuration du dossier principal de stockage
dossier_fichiers = Path("fichiers")
dossier_fichiers.mkdir(exist_ok=True)

# Liste exhaustive de toutes les matières du parcours Sciences et Technologies
categories = [
    "Algèbre Linéaire",
    "Analyse & Calcul Numérique",
    "Thermodynamique",
    "Électromagnétisme & Optique",
    "Mécanique du Point",
    "Chimie Organique & Générale",
    "Informatique (Python & SQL)",
    "Bureautique (Excel, Access)",
    "Sujets de Concours"
]

# Création automatique des sous-dossiers pour chaque matière
for cat in categories:
    (dossier_fichiers / cat).mkdir(exist_ok=True)

# Montage du dossier principal pour le téléchargement
app.mount("/fichiers", StaticFiles(directory="fichiers"), name="fichiers")

@app.get("/", response_class=HTMLResponse)
async def home():
    listes_html = {}
   
    # Récupération dynamique des fichiers pour chaque matière
    for cat in categories:
        chemin_cat = dossier_fichiers / cat
        fichiers_cat = [f.name for f in chemin_cat.iterdir() if f.is_file()]
       
        html_cat = ""
        if not fichiers_cat:
            html_cat = "<p style='color: #64748b; font-style: italic; font-size: 13px; margin: 8px 0;'>Aucun sujet.</p>"
        else:
            html_cat = "<ul style='list-style: none; padding: 0; margin: 0;'>"
            for sujet in fichiers_cat:
                html_cat += f"""
                <li style='background: rgba(255,255,255,0.03); margin: 6px 0; padding: 10px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; border: 1px solid #334155;'>
                    <span style='color: #e2e8f0; font-weight: 500; font-size: 12px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; max-width: 70%;' title='{sujet}'>📄 {sujet}</span>
                    <a href='/fichiers/{cat}/{sujet}' download style='background: #2563eb; color: white; text-decoration: none; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold;'>Ouvrir</a>
                </li>
                """
            html_cat += "</ul>"
        listes_html[cat] = html_cat

    # Options du menu déroulant
    options_select = "".join([f'<option value="{cat}">{cat}</option>' for cat in categories])

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sésame des Techno - Horizon</title>
    <style>
        body {{
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            padding: 20px;
            box-sizing: border-box;
        }}
        .container {{
            max-width: 1200px;
            margin: 10px auto;
            width: 100%;
            background: #1e293b;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            box-sizing: border-box;
        }}
        .header {{ text-align: center; margin-bottom: 25px; }}
        h1 {{ color: #38bdf8; margin: 0 0 5px 0; font-size: 32px; font-weight: 800; }}
        .subtitle {{ color: #94a3b8; margin: 0; font-size: 14px; }}
       
        .upload-section {{
            background: #1e3a8a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border: 1px solid #2563eb;
        }}
        .upload-section h2 {{ font-size: 15px; margin-top: 0; color: #60a5fa; margin-bottom: 12px; font-weight: 600; }}
        .upload-form {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
        }}
        select, input[type="file"] {{
            background: #0f172a;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #475569;
            color: #cbd5e1;
            font-size: 14px;
            flex: 1;
            min-width: 220px;
            box-sizing: border-box;
        }}
        .btn-submit {{
            background: #10b981; color: white; border: none; padding: 11px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; font-size: 14px;
        }}
        .btn-submit:hover {{ background: #059669; }}
       
        /* Grille adaptative pour afficher toutes les matières */
        .grid-categories {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }}
        .card-cat {{
            background: #0f172a;
 
