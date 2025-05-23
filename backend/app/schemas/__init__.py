from app.schemas.offer import (
    OfferBase, OfferCreate, OfferUpdate, 
    OfferInDB, OfferResponse, TechBase
)
from app.schemas.tech import (
    TechBase, TechCreate, TechUpdate, 
    TechInDB, TechWithStats, TechTrend
)
from app.schemas.candidature import (
    CandidatureStatus, CandidatureBase, CandidatureCreate, 
    CandidatureUpdate, CandidatureInDB, CandidatureResponse,
    OfferBasicInfo
)

# Exporter les classes pour faciliter l'importation
__all__ = [
    "OfferBase", "OfferCreate", "OfferUpdate", "OfferInDB", "OfferResponse",
    "TechBase", "TechCreate", "TechUpdate", "TechInDB", "TechWithStats", "TechTrend",
    "CandidatureStatus", "CandidatureBase", "CandidatureCreate", "CandidatureUpdate",
    "CandidatureInDB", "CandidatureResponse", "OfferBasicInfo"
]
