from fastapi import HTTPException, status

class NotFoundError(HTTPException):
    """
    Exception pour les ressources non trouvées
    """
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestError(HTTPException):
    """
    Exception pour les requêtes invalides
    """
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedError(HTTPException):
    """
    Exception pour les accès non autorisés
    """
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenError(HTTPException):
    """
    Exception pour les accès interdits
    """
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ConflictError(HTTPException):
    """
    Exception pour les conflits (ex: ressource déjà existante)
    """
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
