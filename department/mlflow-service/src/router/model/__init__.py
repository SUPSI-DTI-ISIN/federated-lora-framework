from .adapter.routes import router as adapter_router
from .base.routes import router as base_router

__all__ = [
    'adapter_router',
    'base_router'
]

__version__ = "1.0.0"