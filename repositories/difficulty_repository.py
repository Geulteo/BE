from typing import List

from models.difficulty_card import DifficultyCard
from templates.difficulty_templates import DIFFICULTY_CARDS

class DifficultyCardRepository:
    @staticmethod
    def load_all(self) -> List[DifficultyCard]:
        return DIFFICULTY_CARDS