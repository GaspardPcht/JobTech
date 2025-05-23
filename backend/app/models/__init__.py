from app.models.offer import Offer, offer_tech
from app.models.tech import Tech
from app.models.candidature import Candidature, CandidatureStatus

# Exporter les classes pour faciliter l'importation
__all__ = [
    "Offer", 
    "Tech", 
    "Candidature", 
    "CandidatureStatus",
    "offer_tech"
]
