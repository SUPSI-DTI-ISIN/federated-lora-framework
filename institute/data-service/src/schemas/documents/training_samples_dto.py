from pydantic import BaseModel


class TrainingSamplesDTO(BaseModel):
    institute_name: str
    trainable_samples_number: int
