import pytest

from schemas.exceptions.institute_errors import (
    InstituteNotFoundError,
    InstituteNameNotFoundError,
    InstituteCannotBeDeletedError,
    InstituteCannotBeUpdatedError,
    InstituteUnreachableError,
)


class TestInstituteNotFoundError:
    def test_stores_institute_id(self):
        assert InstituteNotFoundError(institute_id=42).institute_id == 42

    def test_message_contains_id(self):
        assert "42" in str(InstituteNotFoundError(institute_id=42))

    def test_is_exception_subclass(self):
        assert issubclass(InstituteNotFoundError, Exception)


class TestInstituteNameNotFoundError:
    def test_stores_institute_name(self):
        assert InstituteNameNotFoundError(institute_name="Alpha").institute_name == "Alpha"

    def test_message_contains_name(self):
        assert "Alpha" in str(InstituteNameNotFoundError(institute_name="Alpha"))

    def test_is_exception_subclass(self):
        assert issubclass(InstituteNameNotFoundError, Exception)


class TestInstituteCannotBeDeletedError:
    def test_stores_institute_id(self):
        assert InstituteCannotBeDeletedError(institute_id=7).institute_id == 7

    def test_message_contains_id(self):
        assert "7" in str(InstituteCannotBeDeletedError(institute_id=7))

    def test_is_exception_subclass(self):
        assert issubclass(InstituteCannotBeDeletedError, Exception)


class TestInstituteCannotBeUpdatedError:
    def test_stores_institute_id(self):
        assert InstituteCannotBeUpdatedError(institute_id=99).institute_id == 99

    def test_message_contains_id(self):
        assert "99" in str(InstituteCannotBeUpdatedError(institute_id=99))

    def test_is_exception_subclass(self):
        assert issubclass(InstituteCannotBeUpdatedError, Exception)


class TestInstituteUnreachableError:
    def test_stores_institute_url(self):
        assert InstituteUnreachableError(institute_url="http://dead.local").institute_url == "http://dead.local"

    def test_message_contains_url(self):
        assert "http://dead.local" in str(InstituteUnreachableError(institute_url="http://dead.local"))

    def test_is_exception_subclass(self):
        assert issubclass(InstituteUnreachableError, Exception)
