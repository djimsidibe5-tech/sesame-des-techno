from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

app = FastAPI(
    title="Horizon - Sésame des Techno",
    version="1.5.0",
    description="Plateforme complète de centralisation Sciences & Technologies"
)

# Configuration du dossier principal de stockage
dossier_fichiers = Path("fichiers")
dossier_fichiers.mkdir(exist_ok=True)

# Liste complète de toutes les matières
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

# Création automatique des dossiers pour chaque matière
for cat in categories:
    (dossier_fichiers / cat).mkdir(exist_ok=True)

# Montage du dossier pour rendre les fichiers téléchargeables
app.mount("/fichiers", StaticFiles(directory="fichiers"), name="fichiers")

@app.get("/", response_class=HTMLResponse)
async def home():
    # Construction dynamique des blocs de matières sans f-string globale (évite les conflits CSS/Python)
    blocs_matieres_html = ""
   
    for cat in categories:
        chemin_cat = dossier_fichiers / cat
        fichiers_cat = [f.name for f in chemin_cat.iterdir() if f.is_file()]
       
        liste_fichiers_html = ""
        if not fichiers_cat:
            liste_fichiers_html = "<p class='no-file'>Aucun sujet disponible.</p>"
        else:
            liste_fichiers_html = "<ul class='file-list'>"
            for sujet in fichiers_cat:
                liste_fichiers_html += f"""
                <li class='file-item'>
                    <span class='file-name' title='{sujet}'>📄 {sujet}</span>
                    <a href='/fichiers/{cat}/{sujet}' download class='btn-download'>Ouvrir</a>
                </li>
                """
            liste_fichiers_html += "</ul>"
           
        # Style spécial pour les concours
        classe_carte = "card-cat special" if cat == "Sujets de Concours" else "card-cat"
       
        blocs_matieres_html += f"""
        <div class='{classe_carte}'>
            <h3>{cat}</h3>
            {liste_fichiers_html}
        </div>
        """

    # Génération des options du formulaire
    options_select = "".join([f'<option value="{cat}">{cat}</option>' for cat in categories])

    # Code HTML pur (plus de f-string globale = zéro bug de syntaxe)
    html_content = """
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
                background-color: #0f172a;
                color: #f8fafc;
                padding: 20px;
                box-sizing: border-box;
            }
            .container {
                max-width: 1200px;
                margin: 10px auto;
                width: 100%;
                background: #1e293b;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.4);
                box-sizing: border-box;
            }
            .header { text-align: center; margin-bottom: 25px; }
            h1 { color: #38bdf8; margin: 0 0 5px 0; font-size: 32px; font-weight: 800; }
            .subtitle { color: #94a3b8; margin: 0; font-size: 14px; }
           
            .upload-section {
                background: #1e3a8a;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                border: 1px solid #2563eb;
            }
            .upload-section h2 { font-size: 15px; margin-top: 0; color: #60a5fa; margin-bottom: 12px; font-weight: 600; }
            .upload-form {
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                align-items: center;
            }
            select, input[type="file"] {
                background: #0f172a;
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #475569;
                color: #cbd5e1;
                font-size: 14px;
                flex: 1;
                min-width: 220px;
                box-sizing: border-box;
            }
            .btn-submit {
                background: #10b981; color: white; border: none; padding: 11px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; font-size: 14px;
            }
            .btn-submit:hover { background: #059669; }
           
            .grid-categories {
                display: grid;
