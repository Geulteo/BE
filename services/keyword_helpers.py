from typing import Any, Dict, Optional, Tuple

# Enum/str 등 어떤 형태로 와도 'request' 같은 문자열로 정규화.
def ensure_str_intent(intent_label: Any) -> Optional[str]:
    if intent_label is None:
        return None
    if hasattr(intent_label, "value"):
        return str(intent_label.value)
    return str(intent_label)

# 전처리 결과에서 SBERT용 문장을 안전하게 확보
def pick_sentence_for_sbert(process_result: Dict[str, Any]) -> str:
    return (
        process_result.get("sentence_for_sbert")
        or process_result.get("sbert_sentence")
        or process_result.get("cleaned_text")
        or ""
    )

def extract_template_info(structure_template: Any) -> Tuple[Optional[str], Any]:
    template_id = None
    template_slots = None

    if isinstance(structure_template, dict):
        template_id = (
            structure_template.get("template_id")
            or structure_template.get("template_name")
            or structure_template.get("id")
        )
        template_slots = (
            structure_template.get("template_slots")
            or structure_template.get("slot_list")
            or structure_template.get("slots")
        )
    elif structure_template is not None:
        template_id = (
            getattr(structure_template, "template_id", None)
            or getattr(structure_template, "template_name", None)
            or getattr(structure_template, "id", None)
        )
        template_slots = (
            getattr(structure_template, "template_slots", None)
            or getattr(structure_template, "slot_list", None)
            or getattr(structure_template, "slots", None)
        )

    return template_id, template_slots

# 응답에 넣을 때 JSON 직렬화 가능한 형태로 변환
def to_jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool, list, dict)):
        return obj
    if hasattr(obj, "model_dump"):
        try:
            return obj.model_dump()
        except Exception:
            pass
    if hasattr(obj, "dict"):
        try:
            return obj.dict()
        except Exception:
            pass
    if hasattr(obj, "__dict__"):
        try:
            return dict(obj.__dict__)
        except Exception:
            pass
    return str(obj)
