from .management_service_interface import ManagementServiceInterface


class ManagementService(ManagementServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    async def start_federated_learning(self):
        print("Start federated learning from service")