from sqlalchemy.orm import DeclarativeBase

from entities.base_model import BaseModel


class TestBaseModel:
    def test_is_declarative_base(self):
        assert issubclass(BaseModel, DeclarativeBase)

    def test_has_metadata(self):
        assert hasattr(BaseModel, "metadata")
