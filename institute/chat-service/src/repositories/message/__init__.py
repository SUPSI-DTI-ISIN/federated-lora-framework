from .message_repository_interface import MessageRepositoryInterface
from .dependencies import get_message_repository, build_message_repository

__all__ = [
    'MessageRepositoryInterface',
    'get_message_repository',
    'build_message_repository'
]

__version__ = "1.0.0"