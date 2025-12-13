# intent별 문장 구성 흐름 (slot)
SLOT_BY_INTENT = {
    "REQUEST": ["상황", "이유", "요청", "마무리"],
    "QUESTION": ["상황", "모르겠는 점", "구체적 질문"],
    "NOTICE": ["배경", "핵심 정보", "변경사항", "마무리"],
    "COMPLAINT": ["문제 상황", "영향", "해결 요청"],
    "APOLOGY": ["상황", "원인", "사과", "후속 조치"],
}

# intent 내부 세부 템플릿 (SBERT 비교 대상)
SUBTEMPLATES = {
    "REQUEST": {
        "request_deadline": "과제나 업무의 마감 기한을 연장해달라고 정중히 부탁하는 상황입니다.",
        "request_absence": "수업이나 약속에 결석하거나 지각하게 되어 양해를 구하는 상황입니다.",
        "request_help": "문제 해결이나 과제 수행을 도와달라고 요청하는 상황입니다.",
        "request_info": "자료나 정보를 보내달라고 부탁하는 상황입니다.",
        "request_schedule": "일정 변경이나 조정을 부탁하는 상황입니다.",
        "request_meeting": "미팅이나 상담 시간을 요청하는 상황입니다.",
        "request_default": "기타 정중한 요청 상황입니다.",
    },

    "QUESTION": {
        "question_procedure": "진행 절차나 방법을 몰라 질문하는 상황입니다.",
        "question_requirement": "필요 조건이나 기준을 확인하기 위한 질문 상황입니다.",
        "question_deadline": "마감 기한이나 일정과 관련해 확인하는 질문입니다.",
        "question_reason": "이유나 배경을 알고 싶어 질문하는 상황입니다.",
        "question_detail": "이미 받은 안내에서 세부 내용을 추가로 묻는 상황입니다.",
        "question_default": "기타 일반적인 질문 상황입니다.",
    },

    "NOTICE": {
        "notice_schedule_change": "일정 변경 사항을 안내하는 상황입니다.",
        "notice_general": "일반적인 공지나 전달 사항을 알리는 상황입니다.",
        "notice_event": "행사나 모임 관련 정보를 안내하는 상황입니다.",
        "notice_policy": "규칙이나 정책 변경 사항을 안내하는 상황입니다.",
        "notice_result": "결과나 처리 상태를 안내하는 상황입니다.",
    },

    "COMPLAINT": {
        "complaint_service": "서비스나 시스템 이용 중 불편 사항을 제기하는 상황입니다.",
        "complaint_error": "오류나 문제 발생에 대해 신고하는 상황입니다.",
        "complaint_delay": "처리가 지연되거나 응답이 늦은 것에 대한 불만 상황입니다.",
        "complaint_attitude": "상대방의 태도나 대응 방식에 대해 불만을 제기하는 상황입니다.",
        "complaint_default": "기타 불만이나 문제 제기 상황입니다.",
    },

    "APOLOGY": {
        "apology_delay": "답변이나 처리가 늦어진 것에 대해 사과하는 상황입니다.",
        "apology_mistake": "본인의 실수나 오류에 대해 사과하는 상황입니다.",
        "apology_inconvenience": "불편을 끼친 것에 대해 사과하는 상황입니다.",
        "apology_miscommunication": "의사 전달이 잘못된 점에 대해 사과하는 상황입니다.",
        "apology_default": "기타 일반적인 사과 상황입니다.",
    },
}
