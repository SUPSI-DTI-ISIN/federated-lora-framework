import pytest
from pydantic import ValidationError

from clients.schemas.institute_training_participation_dto import InstituteTrainingParticipationDTO


class TestClientInstituteTrainingParticipationDTO:
    def test_valid_construction(self):
        dto = InstituteTrainingParticipationDTO(institute_name="Alpha", trainable_samples_number=50)
        assert dto.institute_name == "Alpha"
        assert dto.trainable_samples_number == 50

    @pytest.mark.parametrize("payload", [
        {"institute_name": "Alpha"},
        {"trainable_samples_number": 10},
        {},
    ])
    def test_missing_required_field_raises(self, payload):
        with pytest.raises(ValidationError):
            InstituteTrainingParticipationDTO(**payload)
