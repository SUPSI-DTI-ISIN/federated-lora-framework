import pytest
from pydantic import ValidationError

from schemas.institute.institute_training_participation_dto import InstituteTrainingParticipationDTO


class TestInstituteTrainingParticipationDTO:
    def test_all_fields_set(self):
        dto = InstituteTrainingParticipationDTO(
            id=1, institute_name="Alpha", trainable_samples_number=100, is_reachable=True
        )
        assert dto.id == 1
        assert dto.institute_name == "Alpha"
        assert dto.trainable_samples_number == 100
        assert dto.is_reachable is True

    def test_trainable_samples_number_is_optional(self):
        dto = InstituteTrainingParticipationDTO(
            id=2, institute_name="Beta", trainable_samples_number=None, is_reachable=False
        )
        assert dto.trainable_samples_number is None
        assert dto.is_reachable is False

    def test_missing_required_field_raises(self):
        with pytest.raises(ValidationError):
            InstituteTrainingParticipationDTO(institute_name="X", is_reachable=True)
