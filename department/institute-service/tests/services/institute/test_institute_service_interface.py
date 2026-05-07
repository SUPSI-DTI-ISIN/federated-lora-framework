import pytest

from services.institute.institute_service_interface import InstituteServiceInterface


class TestInstituteServiceInterface:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            InstituteServiceInterface()

    def test_complete_subclass_can_be_instantiated(self):
        class Concrete(InstituteServiceInterface):
            async def create_new_institute(self, dto): ...
            async def update_institute(self, institute_id, dto): ...
            async def get_all(self): ...
            async def get_by_id(self, institute_id): ...
            async def get_by_name(self, institute_name): ...
            async def delete_institute_by_id(self, institute_id): ...
            async def get_institutes_training_participation(self): ...

        assert isinstance(Concrete(), InstituteServiceInterface)

    async def test_abstract_methods_raise_not_implemented(self):
        class CallerThrough(InstituteServiceInterface):
            async def create_new_institute(self, dto):
                return await super().create_new_institute(dto)

            async def update_institute(self, institute_id, dto):
                return await super().update_institute(institute_id, dto)

            async def get_all(self):
                return await super().get_all()

            async def get_by_id(self, institute_id):
                return await super().get_by_id(institute_id)

            async def get_by_name(self, institute_name):
                return await super().get_by_name(institute_name)

            async def delete_institute_by_id(self, institute_id):
                return await super().delete_institute_by_id(institute_id)

            async def get_institutes_training_participation(self):
                return await super().get_institutes_training_participation()

        obj = CallerThrough()

        with pytest.raises(NotImplementedError):
            await obj.create_new_institute(None)
        with pytest.raises(NotImplementedError):
            await obj.update_institute(1, None)
        with pytest.raises(NotImplementedError):
            await obj.get_all()
        with pytest.raises(NotImplementedError):
            await obj.get_by_id(1)
        with pytest.raises(NotImplementedError):
            await obj.get_by_name("x")
        with pytest.raises(NotImplementedError):
            await obj.delete_institute_by_id(1)
        with pytest.raises(NotImplementedError):
            await obj.get_institutes_training_participation()
