from fastapi import Depends, HTTPException, status
from typing import List

from app.models.user import User
from app.utils.security import get_current_active_user

def has_role(required_roles: List[str]):
    """
    Dépendance FastAPI pour vérifier si l'utilisateur a un des rôles requis
    
    Usage:
    @router.get("/admin-only", dependencies=[Depends(has_role(["admin"]))])
    def admin_only_route():
        return {"message": "Vous êtes admin !"}
    """
    async def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès refusé. Rôle requis: {', '.join(required_roles)}"
            )
        return current_user
    
    return role_checker

# Fonctions utilitaires pour les rôles courants
def admin_only(current_user: User = Depends(get_current_active_user)):
    """Vérifie si l'utilisateur est un administrateur"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs"
        )
    return current_user

def premium_or_admin(current_user: User = Depends(get_current_active_user)):
    """Vérifie si l'utilisateur est premium ou administrateur"""
    if current_user.role not in ["premium", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux utilisateurs premium ou administrateurs"
        )
    return current_user
