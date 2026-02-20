from services.management import ManagementServiceInterface, ManagementService


def get_management_service() -> ManagementServiceInterface:
    return ManagementService.get_instance()