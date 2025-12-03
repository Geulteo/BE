from typing import Dict
from pydantic import BaseModel

from core.level_enums import DifficultyLevel


class DifficultyDiagnosisResult(BaseModel):
    # 난이도 진단 결과 (BaseResponse.data 안에 들어갈 payload)
    level: DifficultyLevel
    reason: Dict[str, str]  # structure / info / tone / fluency
