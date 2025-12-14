import json
from pathlib import Path
from typing import List

from models.difficulty_card import DifficultyCard
from templates.difficulty_templates import DIFFICULTY_CARDS


class DifficultyCardRepository:
    def load_all(self) -> List[DifficultyCard]:
        # [수정] JSON 대신 파이썬 상수에서 로드
        return DIFFICULTY_CARDS