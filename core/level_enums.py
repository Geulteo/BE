from enum import Enum

class DifficultyLevel(str, Enum):
    # 훈련 난이도 레벨
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"