from src.models import RefreshToken

async def generate(user_id: int):
    """Generate a new refresh token"""
    token = await RefreshToken.create(user_id)
    return token


async def get_by_token(token: str):
    """Get a refresh token by its value"""
    return await RefreshToken.get_by_token(token)