from typing import List, Dict, Optional
from pydantic import BaseModel
from core.type_enums import IntentType

class IntentResult(BaseModel):
    cleaned_text: str
    keywords: List[str]
    pos_tags: List[str]
    sentence_for_sbert: str

    intent: Optional[IntentType] = None
    intent_scores: Dict[str, float]

    need_more_info: bool
    need_more_info_message: Optional[str] = None