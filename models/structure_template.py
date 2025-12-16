from typing import List, Optional
from pydantic import BaseModel

class StructureTemplateResult(BaseModel):
    template_name: str
    slot_list: List[str]
    score: Optional[float] = None
