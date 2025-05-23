from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import offers, techs, candidatures, imports
from app.routers.external_offers import router as external_offers_router

# Création de l'application FastAPI
app = FastAPI(
    title="JobTech Radar API",
    description="API pour JobTech Radar - Plateforme de recherche d'emploi et d'analyse des tendances tech",
    version="0.1.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # URLs du frontend en développement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(offers, prefix="/api")
app.include_router(techs, prefix="/api")
app.include_router(candidatures, prefix="/api")
app.include_router(imports, prefix="/api")
app.include_router(external_offers_router, prefix="/api")

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
