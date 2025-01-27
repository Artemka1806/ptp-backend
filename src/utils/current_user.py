from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

async def current_user(
    auth: HTTPAuthorizationCredentials = Security(security)
):
    from models import User
    
    if not auth:
        raise HTTPException(401, "No authorization credentials found")
    
    token = auth.credentials
    
    user = await User.get_by_token(token)
    if user is None:
        raise HTTPException(404, "Authorized user could not be found")
    return user