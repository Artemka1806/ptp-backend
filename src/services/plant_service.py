from datetime import datetime

from src.models import Plant, User
from src.schemas.plant import PlantCreate, PlantStatistics

async def create(body: PlantCreate, user: User):
    """Create a new plant"""
    return await Plant.create(body, user.id)


async def get_by_code(code: str):
    """Get a plant by its code"""
    plant = await Plant.get_by_code(code)
    if not plant:
        return None
    return plant.dump()


async def get_by_code_and_owner(code: str, user: User):
    """Get a plant by its code and user"""
    plant = await Plant.get_by_code_and_owner(code, user.id)
    if not plant:
        return None
    return plant.dump()


async def update_by_code(code: str, body: PlantStatistics):
    """Update a plant's statistics by its code"""
    plant = await Plant.get_by_code(code)
    if not plant:
        return None
    return await plant.update_statistics(body)


async def update_advice_by_code_and_owner(code: str, advice: str, user: User):
    """Update a plant's advice by its code and user"""
    plant = await Plant.get_by_code_and_owner(code, user.id)
    if not plant:
        return None
    plant.advice = advice
    plant.advice_updated_at = datetime.utcnow()
    await plant.save()
    return plant.dump()


async def update_weekly_advice_by_code_and_owner(code: str, advice: str, user: User):
    """Update the weekly advice for a specific plant"""
    plant = await Plant.find_one({"code": code, "owner": user.id})
    if not plant:
        return None
    
    plant.weekly_advice = advice
    plant.weekly_advice_updated_at = datetime.utcnow()
    await plant.save()
    return plant


async def update_all_by_code(code: str, body: PlantStatistics):
    """Update all plants with a matching code"""
    plants = await Plant.find(Plant.code == code).to_list()
    if not plants:
        return None
    
    updated_plants = []
    for plant in plants:
        updated_plant = await plant.update_statistics(body)
        updated_plants.append(updated_plant)
        
    return updated_plants


async def delete_by_code(code: str):
    """Delete a plant by its code"""
    plant = await Plant.get_by_code(code)
    if not plant:
        return None
    await plant.delete()
    return plant.dump()


async def delete_by_code_and_owner(code: str, user: User):
    """Delete a plant by its code and user"""
    plant = await Plant.get_by_code_and_owner(code, user.id)
    if not plant:
        return None
    await plant.delete()
    return plant.dump()


async def delete_by_owner_id(owner_id: str):
    """Delete all plants owned by a specific user"""
    plants = await Plant.find(Plant.owner_id == owner_id).to_list()
    if not plants:
        return False
        
    for plant in plants:
        await plant.delete()
        
    return True