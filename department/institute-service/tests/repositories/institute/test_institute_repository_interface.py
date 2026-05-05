import pytest

from repositories.institute.institute_repository_interface import InstituteRepositoryInterface


class TestInstituteRepositoryInterface:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            InstituteRepositoryInterface()

    def test_incomplete_subclass_cannot_be_instantiated(self):
        class Incomplete(InstituteRepositoryInterface):
            pass

        with pytest.raises(TypeError):
            Incomplete()

    def test_complete_subclass_can_be_instantiated(self):
        class Concrete(InstituteRepositoryInterface):
            async def save(self, institute_model): ...
            async def get_all(self): ...
            async def get_by_id(self, institute_id): ...
            async def get_by_name(self, institute_name): ...
            async def delete_institute_by_id(self, institute_model): ...

        assert isinstance(Concrete(), InstituteRepositoryInterface)

    async def test_abstract_methods_raise_not_implemented(self):
        class CallerThrough(InstituteRepositoryInterface):
            async def save(self, institute_model):
                return await super().save(institute_model)

            async def get_all(self):
                return await super().get_all()

            async def get_by_id(self, institute_id):
                return await super().get_by_id(institute_id)

            async def get_by_name(self, institute_name):
                return await super().get_by_name(institute_name)

            async def delete_institute_by_id(self, institute_model):
                return await super().delete_institute_by_id(institute_model)

        obj = CallerThrough()

        with pytest.raises(NotImplementedError):
            await obj.save(None)
        with pytest.raises(NotImplementedError):
            await obj.get_all()
        with pytest.raises(NotImplementedError):
            await obj.get_by_id(1)
        with pytest.raises(NotImplementedError):
            await obj.get_by_name("x")
        with pytest.raises(NotImplementedError):
            await obj.delete_institute_by_id(None)
