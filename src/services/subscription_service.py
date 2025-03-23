from src.models import Subscription, SubscriptionKeys
from src.schemas.subscription import SubscriptionCreate

async def create(body: SubscriptionCreate, user_id: str) -> Subscription:
    """
    Create a new subscription.
    """
    subscription = await Subscription.create(
        endpoint=body.endpoint,
        keys=SubscriptionKeys(**body.keys),
        user_id=user_id,
    )
    return subscription


async def get_by_user_id(user_id: str) -> Subscription | None:
    """
    Get a subscription by user ID.
    """
    return await Subscription.get_by_user_id(user_id=user_id)


async def get_by_endpoint(endpoint: str) -> Subscription | None:
    """
    Get a subscription by endpoint.
    """
    return await Subscription.get_by_endpoint(endpoint=endpoint)
