from typing import Optional

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

async def current_user(
    token: Optional[str] = None,
    auth: HTTPAuthorizationCredentials = Security(security),
):
    from src.models import User

    if token is None:
        if not auth:
            raise HTTPException(401, "No authorization credentials found")
        token = auth.credentials

    user = await User.get_by_token(token)
    if user is None:
        raise HTTPException(404, "Authorized user could not be found")
    return user