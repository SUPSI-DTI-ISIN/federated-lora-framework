from dataclasses import dataclass
from typing import List

from .training_row import TrainingRow

@dataclass
class TrainingDataset:
    training_rows: List[TrainingRow]