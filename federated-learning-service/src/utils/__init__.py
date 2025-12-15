from .settings import Settings
from .file_utils import FileUtils

settings = Settings()

__all__ = [
    'settings',
    'FileUtils',
]

__version__ = "1.0.0"