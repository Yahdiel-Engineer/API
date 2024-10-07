from fastapi import FastAPI
from fastapi.responses import HTMLResponse
# from router import router
# from auth import auth



description = """
Cette API de SIRECOM permet d'accéder, de gérer et de modifier les données essentielles stockées dans la base de données de l'entreprise. Elle offre une interface sécurisée pour interagir avec plusieurs tables, facilitant ainsi les opérations internes et l'optimisation des processus.

## Fonctionnalités principales

### Produits

- **Obtenir un produit par code-barres** : Permet de récupérer les informations détaillées d'un produit en utilisant son code-barres.
- **Voir tous les produits** : Retourne la liste complète des produits disponibles.
- **Modifier la catégorie d'un produit** : Change la catégorie d'un produit en fonction d'un nouvel ID de catégorie.
- **Modifier le prix d'un produit** : Met à jour le prix d'un produit spécifique.
- **Modifier le coût de vente d'un produit** : Permet de mettre à jour le coût de vente d'un produit en fonction de son ID.

L'API est conçue pour offrir une flexibilité maximale dans la gestion des produits tout en assurant la sécurité et l'intégrité des données.
"""



app = FastAPI(title="SirecomApp", 
              description=description,
              version="2.0",
              contact=dict(
                name="Sirecom",
                url="https://sirecomapp.exemple.net/",
                email="sirecom@exemple.com",
    ),
              )



@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bienvenue sur SIRECOM</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
                background-color: #f4f4f4;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            img.logo {
                max-width: 200px;
                margin-bottom: 20px;
            }
            h1 {
                color: #333;
            }
            p {
                color: #555;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: white;
                background-color: #007BFF;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
            }
            .button:hover {
                background-color: #0056b3;
                transform: scale(1.05);
            }
            .button:active {
                background-color: #004494;
                transform: scale(0.95);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="https://sirecom.ma/wp-content/uploads/2017/12/logo-1800px.png" alt="SIRECOM Logo" class="logo">
            <h1>Bienvenue sur SIRECOM</h1>
            <p>Pour accéder à la documentation de l'API, cliquez sur le bouton ci-dessous :</p>
            <a href="/docs" class="button">Accéder à la Documentation</a>
        </div>
    </body>
    </html>
    """





# app.include_router(auth, prefix='/auth',tags=['Authentification'])
# app.include_router(router, prefix="/router", tags=["SIRECOM"])














