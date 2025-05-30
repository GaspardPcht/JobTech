from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import techs, candidatures
from app.routers.external_offers import router as external_offers_router
from app.routers.user import router as auth_router  # Assurez-vous que ce fichier existe
from app.routers.tech_extraction import router as tech_extraction_router

# Création de l'application FastAPI
app = FastAPI(
    title="JobTech Radar API",
    description="API pour JobTech Radar - Plateforme de recherche d'emploi et d'analyse des tendances tech",
    version="0.1.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines en développement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(techs, prefix="/api")
app.include_router(candidatures, prefix="/api")
app.include_router(external_offers_router, prefix="/api")
app.include_router(tech_extraction_router, prefix="/api")
app.include_router(auth_router)  # Le préfixe est déjà défini dans le routeur

@app.get("/")
async def root():
    """
    Route racine de l'API qui renvoie un message de bienvenue
    """
    return {"message": "Bienvenue sur l'API JobTech Radar"}

@app.get("/api/health")
async def health_check():
    """
    Endpoint de vérification de santé de l'API
    """
    return {"status": "ok", "version": app.version}
