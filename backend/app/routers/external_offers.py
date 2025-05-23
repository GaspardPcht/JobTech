from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.integrations.adzuna import AdzunaClient
from app.integrations.pole_emploi import PoleEmploiClient
from app.schemas.offer import OfferResponse

router = APIRouter(
    prefix="/external-offers",
    tags=["external-offers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[OfferResponse])
async def search_external_offers(
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    contract_type: Optional[str] = None,
    remote: Optional[bool] = None,
    sources: Optional[str] = "all",  # "all", "adzuna", "pole-emploi"
    limit: int = 20
):
    """
    Recherche des offres d'emploi directement auprès des API externes (Pôle Emploi, Adzuna)
    sans les stocker dans la base de données locale.
    """
    results = []
    
    # Déterminer quelles sources utiliser
    use_adzuna = sources.lower() in ["all", "adzuna"]
    use_pole_emploi = sources.lower() in ["all", "pole-emploi"]
    
    # Recherche sur Adzuna
    if use_adzuna:
        try:
            adzuna_client = AdzunaClient()
            adzuna_response = adzuna_client.search_offers(
                keywords=keywords,
                location=location,
                per_page=limit
            )
            
            # Convertir les offres Adzuna en schéma OfferResponse
            for offer_data in adzuna_response.get("results", []):
                offer_schema = adzuna_client.map_to_offer_schema(offer_data)
                
                # Filtrer par type de contrat si spécifié
                if contract_type and offer_schema.contract_type != contract_type:
                    continue
                
                # Filtrer par remote si spécifié
                if remote is not None and offer_schema.remote != remote:
                    continue
                
                # Convertir en OfferResponse
                offer_response = OfferResponse(
                    id=0,  # ID fictif car non stocké en base
                    title=offer_schema.title,
                    company=offer_schema.company,
                    location=offer_schema.location,
                    description=offer_schema.description,
                    salary_min=offer_schema.salary_min,
                    salary_max=offer_schema.salary_max,
                    contract_type=offer_schema.contract_type,
                    remote=offer_schema.remote,
                    url=offer_schema.url,
                    posted_at=datetime.now(),  # Utiliser la date actuelle car posted_at n'existe pas dans OfferCreate
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    techs=[tech for tech in offer_schema.techs] if hasattr(offer_schema, 'techs') else []
                )
                
                results.append(offer_response)
        except Exception as e:
            print(f"Erreur lors de la recherche sur Adzuna: {str(e)}")
    
    # Recherche sur Pôle Emploi
    if use_pole_emploi:
        try:
            pole_emploi_client = PoleEmploiClient()
            pole_emploi_response = pole_emploi_client.search_offers(
                keywords=keywords,
                location=location,
                per_page=limit
            )
            
            # Convertir les offres Pôle Emploi en schéma OfferResponse
            for offer_data in pole_emploi_response.get("resultats", []):
                offer_schema = pole_emploi_client.map_to_offer_schema(offer_data)
                
                # Filtrer par type de contrat si spécifié
                if contract_type and offer_schema.contract_type != contract_type:
                    continue
                
                # Filtrer par remote si spécifié
                if remote is not None and offer_schema.remote != remote:
                    continue
                
                # Convertir en OfferResponse
                offer_response = OfferResponse(
                    id=0,  # ID fictif car non stocké en base
                    title=offer_schema.title,
                    company=offer_schema.company,
                    location=offer_schema.location,
                    description=offer_schema.description,
                    salary_min=offer_schema.salary_min,
                    salary_max=offer_schema.salary_max,
                    contract_type=offer_schema.contract_type,
                    remote=offer_schema.remote,
                    url=offer_schema.url,
                    posted_at=datetime.now(),  # Utiliser la date actuelle car posted_at n'existe pas dans OfferCreate
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    techs=[tech for tech in offer_schema.techs] if hasattr(offer_schema, 'techs') else []
                )
                
                results.append(offer_response)
        except Exception as e:
            print(f"Erreur lors de la recherche sur Pôle Emploi: {str(e)}")
    
    # Limiter le nombre de résultats
    return results[:limit]
