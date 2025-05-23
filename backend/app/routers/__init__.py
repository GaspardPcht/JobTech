# Importer les routers directement pour faciliter l'importation
from app.routers.offers import router as offers
from app.routers.techs import router as techs
from app.routers.candidatures import router as candidatures
from app.routers.imports import router as imports

# Cela permet d'importer les routers comme:
# from app.routers import offers, techs, candidatures, imports
