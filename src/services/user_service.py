from src.models import User

async def get_plants(user: User):
    plants = await user.get_plants()
    return {"plants": [plant.dump() for plant in plants]}
