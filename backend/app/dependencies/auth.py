from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.utils.security import decode_token
from app.utils.exceptions import UnauthorizedException, ForbiddenException
from typing import List

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise UnauthorizedException("Invalid or expired token")
        
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Token missing subject")
        
    import uuid
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise UnauthorizedException("Invalid token subject format")
        
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_uuid)
    
    if not user:
        raise UnauthorizedException("User not found")
        
    if user.status != "active":
        raise UnauthorizedException("Account is deactivated")
        
    return user

def require_role(roles: List[str]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise ForbiddenException(f"Insufficient permissions. Required role: {', '.join(roles)}")
        return current_user
    return role_checker
