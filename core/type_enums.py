from enum import Enum

class IntentType(str, Enum):
    # 상황 유형
    REQUEST = "request"
    QUESTION = "question"
    NOTICE = "notice"
    COMPLAINT = "complaint"
    APOLOGY = "apology"


class TemplateId(str, Enum):
    # REQUEST
    REQUEST_DEADLINE = "request_deadline"
    REQUEST_ABSENCE = "request_absence"
    REQUEST_HELP = "request_help"
    REQUEST_INFO = "request_info"
    REQUEST_SCHEDULE = "request_schedule"
    REQUEST_MEETING = "request_meeting"
    REQUEST_DEFAULT = "request_default"

    # QUESTION
    QUESTION_PROCEDURE = "question_procedure"
    QUESTION_REQUIREMENT = "question_requirement"
    QUESTION_DEADLINE = "question_deadline"
    QUESTION_REASON = "question_reason"
    QUESTION_DETAIL = "question_detail"
    QUESTION_DEFAULT = "question_default"

    # NOTICE
    NOTICE_SCHEDULE_CHANGE = "notice_schedule_change"
    NOTICE_GENERAL = "notice_general"
    NOTICE_EVENT = "notice_event"
    NOTICE_POLICY = "notice_policy"
    NOTICE_RESULT = "notice_result"

    # COMPLAINT
    COMPLAINT_SERVICE = "complaint_service"
    COMPLAINT_ERROR = "complaint_error"
    COMPLAINT_DELAY = "complaint_delay"
    COMPLAINT_ATTITUDE = "complaint_attitude"
    COMPLAINT_DEFAULT = "complaint_default"

    # APOLOGY
    APOLOGY_DELAY = "apology_delay"
    APOLOGY_MISTAKE = "apology_mistake"
    APOLOGY_INCONVENIENCE = "apology_inconvenience"
    APOLOGY_MISCOMMUNICATION = "apology_miscommunication"
    APOLOGY_DEFAULT = "apology_default"

class TargetType(str, Enum):
    PROFESSOR = "professor"        # 교수님
    SENIOR_JUNIOR = "senior_junior" # 선/후배
    FRIEND = "friend"              # 친구
    BOSS = "boss"                  # 직장 상사