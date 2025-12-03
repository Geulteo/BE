from enum import Enum

class IntentType(str, Enum):
    # 상황 유형
    REQUEST = "request"
    QUESTION = "question"
    NOTICE = "notice"
    COMPLAINT = "complaint"
    APOLOGY = "apology"


class TemplateId(str, Enum):
    # 템플릿 유형 - 안적혀 있는 부분 유형들 추후에 추가할 예정
    REQUEST_DEADLINE = "request_deadline"   # 마감/기한 연장 요청
    REQUEST_ABSENCE = "request_absence"     # 결석/지각 양해 요청
    REQUEST_HELP = "request_help"           # 과제/업무 도움 요청
    REQUEST_INFO = "request_info"           # 자료 요청
    REQUEST_DEFAULT = "request_default"     # 기타 요청