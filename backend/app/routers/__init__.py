# Importer les routers directement pour faciliter l'importation
from app.routers.techs import router as techs
from app.routers.candidatures import router as candidatures

# Cela permet d'importer les routers comme:
# from app.routers import techs, candidatures
