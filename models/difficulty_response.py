from typing import Dict
from pydantic import BaseModel

from core.level_enums import DifficultyLevel


class DifficultyDiagnosisResult(BaseModel):
    level: DifficultyLevel
    reason: Dict[str, str]
