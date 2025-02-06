from src.models import Plant, PlantCreate, PlantStatistics, User

async def create(body: PlantCreate, user: User):
    """Create a new plant"""
    return await Plant.create(body, user.id)


async def get_by_code(code: str):
    """Get a plant by its code"""
    plant = await Plant.get_by_code(code)
    if not plant:
        return None
    return plant.dump()


async def update_by_code(code: str, body: PlantStatistics):
    """Update a plant's statistics by its code"""
    plant = await Plant.get_by_code(code)
    if not plant:
        return None
    return await plant.update_statistics(body)