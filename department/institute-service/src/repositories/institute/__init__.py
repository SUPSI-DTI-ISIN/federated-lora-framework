from .institute_repository_interface import InstituteRepositoryInterface
from .dependencies import get_institute_repository, build_institute_repository

__all__ = [
    'InstituteRepositoryInterface',
    'get_institute_repository',
    'build_institute_repository'
]

__version__ = "1.0.0"