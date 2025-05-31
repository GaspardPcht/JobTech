from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.security import get_current_active_user
from app.utils.role_checker import has_role, admin_only, premium_or_admin

router = APIRouter(prefix="/api/protected", tags=["protected"])

@router.get("/user-info")
async def get_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Route protégée accessible à tous les utilisateurs authentifiés
    Retourne les informations de l'utilisateur connecté
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }

@router.get("/admin", dependencies=[Depends(admin_only)])
async def admin_only_route():
    """
    Route protégée accessible uniquement aux administrateurs
    """
    return {"message": "Vous avez accès à cette route car vous êtes administrateur"}

@router.get("/premium", dependencies=[Depends(premium_or_admin)])
async def premium_route():
    """
    Route protégée accessible aux utilisateurs premium et administrateurs
    """
    return {"message": "Vous avez accès à cette route car vous êtes premium ou administrateur"}

@router.get("/role-based/{role_name}", dependencies=[Depends(has_role(["admin", "moderator"]))])
async def role_based_route(role_name: str):
    """
    Route protégée accessible aux utilisateurs ayant le rôle admin ou moderator
    """
    return {"message": f"Vous avez accès à la route pour le rôle {role_name}"}
