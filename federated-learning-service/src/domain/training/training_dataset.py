import json
from dataclasses import dataclass, asdict
from typing import List

from .training_row import TrainingRow


@dataclass
class TrainingDataset:
    data: List[TrainingRow]

    def to_jsonl(self, output_path: str) -> None:
        with open(output_path, 'w', encoding='utf-8') as output:
            for example in self.data:
                output.write(json.dumps(asdict(example), ensure_ascii=False) + '\n')