import pytest

from clients.institute.institute_node_client_interface import InstituteNodeClientInterface


class TestInstituteNodeClientInterface:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            InstituteNodeClientInterface()

    def test_concrete_subclass_can_be_instantiated(self):
        class Concrete(InstituteNodeClientInterface):
            async def get_institute_training_participation(self, institute_base_url: str):
                raise NotImplementedError

        assert isinstance(Concrete(), InstituteNodeClientInterface)

    async def test_abstract_method_raises_not_implemented(self):
        class CallerThrough(InstituteNodeClientInterface):
            async def get_institute_training_participation(self, institute_base_url: str):
                return await super().get_institute_training_participation(institute_base_url)

        with pytest.raises(NotImplementedError):
            await CallerThrough().get_institute_training_participation("http://x.local")
