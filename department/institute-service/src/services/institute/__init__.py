from .institute_service_interface import InstituteServiceInterface
from .dependencies import get_institute_service, build_institute_service

__all__ = [
    'InstituteServiceInterface',
    'get_institute_service',
    'build_institute_service'
]

__version__ = "1.0.0"