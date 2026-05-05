from entities.institute_model import InstituteModel
from entities.base_model import BaseModel


class TestInstituteModel:
    def test_tablename(self):
        assert InstituteModel.__tablename__ == "institutes"

    def test_inherits_base_model(self):
        assert issubclass(InstituteModel, BaseModel)

    def test_column_names(self):
        columns = {col.name for col in InstituteModel.__table__.columns}
        assert columns == {"id", "name", "url", "deletable", "updatable"}

    def test_id_is_primary_key(self):
        assert InstituteModel.__table__.c["id"].primary_key is True

    def test_name_is_unique(self):
        assert InstituteModel.__table__.c["name"].unique is True

    def test_attribute_assignment(self):
        model = InstituteModel()
        model.id = 1
        model.name = "Test"
        model.url = "http://test.local"
        model.deletable = True
        model.updatable = False

        assert model.id == 1
        assert model.name == "Test"
        assert model.url == "http://test.local"
        assert model.deletable is True
        assert model.updatable is False
