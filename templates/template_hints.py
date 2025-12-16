TEMPLATE_HINTS = {
  # REQUEST
  "request_deadline": {
    "must_like_advanced": ["기존 마감일", "희망 제출일"],  # 둘 다 있으면 고급 쪽으로
    "nice_to_have": ["과제명", "수업명", "사유", "대안", "양해", "감사"],
    "extra_checklist": [
      "기존 마감일과 희망 제출일이 모두 포함된다",
      "과제명/수업명 등 요청 대상이 명확하다",
    ],
  },
  "request_absence": {
    "must_like_advanced": ["결석/지각 사유", "대체 방안"],  # 예: 병원/가정사정 + 보강/자료확인
    "nice_to_have": ["결석", "지각", "병원", "진료", "보강", "자료", "과제", "확인"],
    "extra_checklist": [
      "결석/지각 사유가 구체적으로 언급된다",
      "후속 조치(자료 확인/대체 등)가 포함된다",
    ],
  },
  "request_help": {
    "must_like_advanced": ["시도한 내용", "막힌 지점"],  # 도움 요청은 '내가 어디까지 했는지'가 고급 포인트
    "nice_to_have": ["코드", "오류", "로그", "환경", "기한", "원하는 도움 형태"],
    "extra_checklist": [
      "시도한 내용과 막힌 지점이 정리되어 있다",
      "원하는 도움(설명/예시/코드 등)이 구체적이다",
    ],
  },
  "request_info": {
    "must_like_advanced": ["원하는 자료 범위", "형식/마감"],  # 자료 요청은 범위+형식이 고급 포인트
    "nice_to_have": ["파일", "링크", "문서", "자료", "형식", "마감", "용도"],
    "extra_checklist": [
      "요청하는 자료의 범위/형식이 명확하다",
      "필요한 시점(마감/언제까지)이 포함된다",
    ],
  },
  "request_schedule": {
    "must_like_advanced": ["기존 일정", "대체 일정"],  # 일정조정은 before/after가 핵심
    "nice_to_have": ["가능", "불가", "시간", "날짜", "변경", "대안", "확인"],
    "extra_checklist": [
      "기존 일정과 변경 희망 일정이 모두 언급된다",
      "상대 선택지를 고려한 대안이 포함된다",
    ],
  },
  "request_meeting": {
    "must_like_advanced": ["목적", "후보 시간"],  # 미팅 요청은 목적+후보시간이 핵심
    "nice_to_have": ["미팅", "상담", "시간", "가능", "후보", "안건", "목적"],
    "extra_checklist": [
      "미팅 목적/안건이 명확하다",
      "가능한 시간 후보를 2개 이상 제시한다",
    ],
  },
  "request_default": {
    "nice_to_have": ["상황", "이유", "요청", "감사/양해"],
    "extra_checklist": [
      "상황-이유-요청-마무리 흐름이 자연스럽다",
    ],
  },

  # QUESTION
  "question_procedure": {
    "must_like_advanced": ["현재 단계", "막힌 단계"],
    "nice_to_have": ["절차", "순서", "방법", "어디까지", "다음"],
    "extra_checklist": [
      "현재 어디까지 진행했는지 포함된다",
      "어느 단계에서 막혔는지 명확하다",
    ],
  },
  "question_requirement": {
    "must_like_advanced": ["기준", "조건"],
    "nice_to_have": ["요건", "기준", "필요", "가능", "제한", "정책"],
    "extra_checklist": [
      "확인하려는 기준/조건이 명확하다",
    ],
  },
  "question_deadline": {
    "must_like_advanced": ["정확한 날짜", "관련 작업/과제명"],
    "nice_to_have": ["마감", "언제", "까지", "일정", "제출"],
    "extra_checklist": [
      "어떤 일정/과제의 마감인지 명확하다",
      "기준이 되는 날짜/시간이 포함된다",
    ],
  },
  "question_reason": {
    "must_like_advanced": ["배경", "근거"],
    "nice_to_have": ["이유", "왜", "배경", "근거", "정책"],
    "extra_checklist": [
      "배경 맥락과 함께 이유를 묻는다",
    ],
  },
  "question_detail": {
    "must_like_advanced": ["받은 안내", "추가로 궁금한 항목"],
    "nice_to_have": ["추가", "세부", "구체", "안내", "내용"],
    "extra_checklist": [
      "기존 안내(전제)를 언급하고 추가 질문한다",
    ],
  },
  "question_default": {"extra_checklist": ["질문이 구체적이고 답변 범위가 명확하다"]},

  # NOTICE
  "notice_schedule_change": {
    "must_like_advanced": ["변경 전", "변경 후"],
    "nice_to_have": ["일정", "변경", "시간", "날짜", "장소", "사유"],
    "extra_checklist": [
      "변경 전/후 일정이 모두 명시된다",
      "수신자가 해야 할 행동이 포함된다",
    ],
  },
  "notice_general": {
    "nice_to_have": ["대상", "일정", "안내", "공지"],
    "extra_checklist": ["핵심 정보(무엇/언제/어디/대상)가 명확하다"],
  },
  "notice_event": {
    "must_like_advanced": ["일시", "장소"],
    "nice_to_have": ["행사", "모임", "참여", "신청", "문의"],
    "extra_checklist": ["참여 방법/신청 방식이 포함된다"],
  },
  "notice_policy": {
    "must_like_advanced": ["변경 내용", "적용 시점"],
    "nice_to_have": ["정책", "규칙", "변경", "적용", "대상"],
    "extra_checklist": ["적용 대상과 적용 시점이 명확하다"],
  },
  "notice_result": {
    "must_like_advanced": ["결과", "다음 단계"],
    "nice_to_have": ["처리", "완료", "결과", "안내", "후속"],
    "extra_checklist": ["후속 조치/문의 채널이 포함된다"],
  },

  # COMPLAINT
  "complaint_service": {
    "must_like_advanced": ["발생 시점", "불편 영향"],
    "nice_to_have": ["서비스", "불편", "이용", "개선", "요청"],
    "extra_checklist": ["어떤 기능에서 어떤 불편이 있었는지 구체적이다"],
  },
  "complaint_error": {
    "must_like_advanced": ["재현 방법", "오류 메시지/로그"],
    "nice_to_have": ["오류", "에러", "로그", "재현", "버전", "환경"],
    "extra_checklist": ["재현 절차와 오류 증빙이 포함된다"],
  },
  "complaint_delay": {
    "must_like_advanced": ["요청 시점", "지연 기간"],
    "nice_to_have": ["지연", "응답", "처리", "언제", "까지"],
    "extra_checklist": ["지연된 항목과 기간이 명확하다"],
  },
  "complaint_attitude": {
    "must_like_advanced": ["발생 상황", "개선 요청"],
    "nice_to_have": ["태도", "응대", "불쾌", "개선", "요청"],
    "extra_checklist": ["문제 상황을 비난보다 사실 중심으로 설명한다"],
  },
  "complaint_default": {"extra_checklist": ["문제-영향-해결요청 구조가 갖춰져 있다"]},

  # APOLOGY
  "apology_delay": {
    "must_like_advanced": ["지연 사유", "해결 일정"],
    "nice_to_have": ["지연", "늦어", "죄송", "오늘", "내일", "까지"],
    "extra_checklist": ["언제까지 처리/회신할지 일정이 포함된다"],
  },
  "apology_mistake": {
    "must_like_advanced": ["실수 내용", "재발 방지"],
    "nice_to_have": ["실수", "오류", "정정", "다음부터", "재발"],
    "extra_checklist": ["실수 인정 + 재발 방지 약속이 포함된다"],
  },
  "apology_inconvenience": {
    "must_like_advanced": ["불편 영향", "보상/조치"],
    "nice_to_have": ["불편", "죄송", "조치", "해결", "개선"],
    "extra_checklist": ["불편을 줄이기 위한 조치를 제시한다"],
  },
  "apology_miscommunication": {
    "must_like_advanced": ["혼선 원인", "정확한 재안내"],
    "nice_to_have": ["의사소통", "혼선", "정정", "다시", "안내"],
    "extra_checklist": ["정확한 정보로 재안내한다"],
  },
  "apology_default": {"extra_checklist": ["상황-원인-사과-후속조치가 포함된다"]},
}
