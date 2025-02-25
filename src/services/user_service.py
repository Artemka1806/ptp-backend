from src.models import User

async def create(email: str, name: str, hashed_password: str):
    """Create a new user"""
    user = await User.get_by_email(email)
    if user:
        return None

    return await User.create(email, name, hashed_password)


async def delete(user: User):
    """Delete a user and all their data"""
    return await user.delete_user()


async def get_by_id(id: int):
    """Get a user by their ID"""
    return await User.get_by_id(id)


async def get_by_email(email: str):
    """Get a user by their email"""
    return await User.get_by_email(email)


async def get_plants(user: User):
    """Get all plants owned by a user"""
    plants = await user.get_plants()
    return {"plants": [plant.dump() for plant in plants]}
