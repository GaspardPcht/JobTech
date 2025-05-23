import uvicorn
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

if __name__ == "__main__":
    # Récupérer les paramètres de configuration depuis les variables d'environnement
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    # Lancer le serveur
    uvicorn.run("app.main:app", host=host, port=port, reload=debug)
