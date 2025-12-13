from __future__ import annotations
from typing import Dict, List
from core.type_enums import IntentType

# 1) 템플릿 문장 정의

INTENT_TEMPLATES: Dict[IntentType, List[str]] = {
    IntentType.REQUEST: [
        "도움을 요청하는 상황입니다.",
        "상대방에게 무언가를 부탁하려는 상황입니다.",
        "양해를 구하고 싶은 상황입니다.",
        "일정 변경이나 연장을 부탁하는 상황입니다.",
        "상대방에게 필요한 도움을 청하는 상황입니다.",
    ],
    IntentType.QUESTION: [
        "궁금한 점을 묻는 상황입니다.",
        "정보를 질문하는 상황입니다.",
        "어떤 내용을 확인하고 싶어 하는 상황입니다.",
        "정확한 답변을 얻기 위해 문의하는 상황입니다.",
        "모르는 부분을 설명해 달라고 요청하는 상황입니다.",
    ],
    IntentType.NOTICE: [
        "중요한 정보를 안내하는 상황입니다.",
        "상대방에게 변경 사항을 알리는 상황입니다.",
        "필요한 내용을 공지하는 상황입니다.",
        "상대방에게 전달해야 할 내용을 정리하는 상황입니다.",
        "상황과 정보를 공유하는 안내 메시지입니다.",
    ],
    IntentType.APOLOGY: [
        "실수나 잘못에 대해 사과하는 상황입니다.",
        "상대방에게 미안한 마음을 전달하는 상황입니다.",
        "불편을 끼쳐 드려 죄송함을 표현하는 상황입니다.",
        "상황을 설명하며 사과하고 싶은 상황입니다.",
        "상대방에게 정중히 사과드리는 메시지입니다.",
    ],
    IntentType.COMPLAINT: [
        "문제점을 지적하는 상황입니다.",
        "불편 사항을 신고하는 상황입니다.",
        "상대방에게 개선을 요구하는 상황입니다.",
        "서비스나 상황에 대해 항의하는 메시지입니다.",
        "해결이 필요한 문제를 전달하는 상황입니다.",
    ],
}

# 2) Rule-based Boost 설정

INTENT_KEYWORD_BOOST = {
    IntentType.REQUEST: ["부탁", "가능", "연장", "도움", "요청", "양해"],
    IntentType.QUESTION: ["무엇", "왜", "어떻게", "궁금", "확인"],
    IntentType.NOTICE: ["공지", "안내", "변경", "취소", "업데이트"],
    IntentType.APOLOGY: ["죄송", "사과", "미안"],
    IntentType.COMPLAINT: ["불편", "문제", "오류", "항의", "답변없"],
}

INTENT_KEYWORD_WEIGHT = {
    IntentType.REQUEST: 0.15,
    IntentType.QUESTION: 0.15,
    IntentType.NOTICE: 0.15,
    IntentType.APOLOGY: 0.20,
    IntentType.COMPLAINT: 0.20,
}

# 3) Threshold

TOP_THRESHOLD = 0.40
DIFF_THRESHOLD = 0.06
TOP_K = 3