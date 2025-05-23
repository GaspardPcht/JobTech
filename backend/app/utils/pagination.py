from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel
from fastapi import Query

T = TypeVar('T')

class PaginationParams:
    """
    Classe utilitaire pour gérer les paramètres de pagination
    """
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
        limit: int = Query(100, ge=1, le=100, description="Nombre maximum d'éléments à retourner")
    ):
        self.skip = skip
        self.limit = limit

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Réponse paginée générique pour les listes d'éléments
    """
    items: List[T]
    total: int
    skip: int
    limit: int
    
    @property
    def has_more(self) -> bool:
        """
        Indique s'il y a plus d'éléments disponibles
        """
        return self.skip + len(self.items) < self.total
