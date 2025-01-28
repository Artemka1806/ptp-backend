__all__ = [
    'ALL_ROUTERS'
]

from .v1 import ALL_ROUTERS as v1_routers

ALL_ROUTERS = [ 
    *v1_routers 
]