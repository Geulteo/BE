from __future__ import annotations
from typing import List

from models.difficulty_card import DifficultyCard
from core.type_enums import IntentType, TemplateId
from core.level_enums import DifficultyLevel


DIFFICULTY_CARDS: List[DifficultyCard] = [
    # =========================================================
    # REQUEST_DEADLINE (마감/기한 연장 요청)
    # =========================================================
    DifficultyCard(
        id="request_deadline_beginner_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEADLINE,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 단순 마감 연장 요청",
        guide="이유는 간단히만 언급하고, 과제명이나 정확한 마감일 언급이 부족한 경우.",
        hint="이유는 있으나 과제/날짜 정보가 거의 없는 기본 수준의 연장 요청입니다.",
        checklist=[
            "이유가 매우 짧게만 언급된다",
            "과제명/수업명/정확한 날짜가 명시되지 않는다",
            "문장이 1~2개로 아주 짧다",
        ],
    ),
    DifficultyCard(
        id="request_deadline_intermediate_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEADLINE,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 이유와 일정이 어느 정도 정리된 연장 요청",
        guide="수업명 또는 과제명을 언급하고, 구체적인 사유와 날짜를 포함하지만 대안 제시는 부족한 경우.",
        hint="수업명/이유/날짜는 포함되어 있지만, 희망 제출일 등 대안이 부족한 단계입니다.",
        checklist=[
            "수업명 또는 과제명이 나온다",
            "구체적인 이유가 포함된다(예: 병원 진료)",
            "현재 마감일 또는 날짜 정보가 포함된다",
        ],
    ),
    DifficultyCard(
        id="request_deadline_advanced_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEADLINE,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 대안과 배려까지 포함한 연장 요청",
        guide="과제명, 마감일, 희망 제출일, 수업 운영에 대한 배려 표현까지 포함된 정중한 요청.",
        hint="과제명/마감/희망일/배려 표현이 모두 포함된 완성도 높은 연장 요청입니다.",
        checklist=[
            "과제명/수업명이 명확하다",
            "기존 마감일과 희망 제출일이 모두 나온다",
            "정중한 표현과 감사/사과, 배려가 포함된다",
        ],
    ),

    # =========================================================
    # REQUEST_ABSENCE (결석/지각 양해 요청)
    # =========================================================
    DifficultyCard(
        id="request_absence_beginner_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_ABSENCE,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 결석/지각 양해 요청(정보 부족)",
        guide="결석/지각 사실만 말하고, 사유·대안·후속 조치가 거의 없는 경우.",
        hint="못 간다는 말은 했지만 이유/대안이 부족한 기본 수준의 양해 요청입니다.",
        checklist=[
            "결석/지각 여부만 짧게 언급된다",
            "이유가 없거나 매우 단순하다",
            "수업/약속 정보(언제/무슨 수업)가 명확하지 않다",
        ],
    ),
    DifficultyCard(
        id="request_absence_intermediate_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_ABSENCE,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 사유와 일정 포함된 결석/지각 양해 요청",
        guide="언제 어떤 수업/약속인지와 사유를 포함하나, 보완 행동(자료 확인/과제 대체 등)이 부족한 경우.",
        hint="언제/왜 못 오는지는 말했지만, 이후 어떻게 할지 제시가 부족한 단계입니다.",
        checklist=[
            "수업/약속명 또는 일정(날짜/시간)이 포함된다",
            "구체적인 사유가 포함된다(예: 병원/가정 사정)",
            "양해 표현은 있으나 후속 조치가 약하다",
        ],
    ),
    DifficultyCard(
        id="request_absence_advanced_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_ABSENCE,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 후속 조치까지 포함한 결석/지각 양해 요청",
        guide="결석/지각 사유와 일정, 그리고 보완 계획(자료 확인/대체 과제/다음 수업 준비)을 함께 제시하는 경우.",
        hint="양해 요청 + 책임 있는 후속 조치까지 포함된 완성형입니다.",
        checklist=[
            "언제/어떤 일정인지 명확하다",
            "사유가 구체적이고 정중하게 전달된다",
            "후속 조치(자료/수업 내용 확인, 과제 대체 등)가 포함된다",
        ],
    ),

    # =========================================================
    # REQUEST_HELP (과제/업무 도움 요청)
    # =========================================================
    DifficultyCard(
        id="request_help_beginner_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_HELP,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 도움 요청(요구만 있고 맥락 부족)",
        guide="도움이 필요하다는 말만 있고, 어떤 부분이 막혔는지/무엇을 시도했는지 정보가 부족한 경우.",
        hint="도와달라고는 했지만 '어디가' 어려운지 설명이 부족한 단계입니다.",
        checklist=[
            "요청만 있고 구체적 문제 설명이 없다",
            "과제/업무 맥락(주제/목표)이 불명확하다",
            "시도한 내용이 없다",
        ],
    ),
    DifficultyCard(
        id="request_help_intermediate_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_HELP,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 문제 구간을 설명한 도움 요청",
        guide="과제/업무 맥락과 막히는 지점은 설명하되, 시도한 방법/현재 상태 정리가 부족한 경우.",
        hint="막힌 지점은 말했지만, 시도/현재 상태가 덜 정리된 단계입니다.",
        checklist=[
            "과제/업무 주제 또는 요구사항이 언급된다",
            "막히는 지점(오류/개념/단계)이 설명된다",
            "시도한 내용 또는 현재 진행 상태가 일부 포함된다",
        ],
    ),
    DifficultyCard(
        id="request_help_advanced_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_HELP,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 시도 내용 + 구체 질문이 포함된 도움 요청",
        guide="맥락, 시도한 방법, 현재 상태, 원하는 도움(구체 질문/요청 범위)을 명확히 제시한 경우.",
        hint="상대가 바로 도와줄 수 있도록 정보가 잘 갖춰진 완성형 도움 요청입니다.",
        checklist=[
            "맥락(과제/업무 목적)과 현재 상태가 정리되어 있다",
            "시도한 방법/결과가 포함된다(로그/에러/과정 등)",
            "원하는 도움의 형태가 구체적이다(무엇을/어떻게)",
        ],
    ),

    # =========================================================
    # REQUEST_INFO (자료 요청)
    # =========================================================
    DifficultyCard(
        id="request_info_beginner_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_INFO,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 자료 요청(대상/범위 불명확)",
        guide="자료를 달라고만 하고 어떤 자료인지, 범위/형식/기한이 없는 경우.",
        hint="요청은 했지만 상대가 뭘 줘야 할지 애매한 단계입니다.",
        checklist=[
            "요청 자료가 구체적으로 특정되지 않는다",
            "범위/형식(파일/링크 등)이 없다",
            "언제까지 필요한지 기한 정보가 없다",
        ],
    ),
    DifficultyCard(
        id="request_info_intermediate_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_INFO,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 자료 종류/용도는 있으나 조건이 부족한 요청",
        guide="요청 자료의 종류나 용도는 말하지만, 범위/형식/기한 중 일부가 부족한 경우.",
        hint="무슨 자료인지는 알겠는데, 전달 조건이 덜 정리된 단계입니다.",
        checklist=[
            "요청 자료(예: 강의자료/문서/파일)가 어느 정도 특정된다",
            "용도 또는 필요한 이유가 포함된다",
            "범위/형식/기한 중 1개 이상이 부족하다",
        ],
    ),
    DifficultyCard(
        id="request_info_advanced_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_INFO,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 범위/형식/기한까지 명확한 자료 요청",
        guide="요청 자료의 범위, 전달 형식, 필요한 시점(기한)을 명확히 하고 감사 표현까지 포함한 경우.",
        hint="상대가 바로 제공할 수 있도록 조건이 완벽히 정리된 자료 요청입니다.",
        checklist=[
            "요청 자료의 범위가 명확하다(어느 부분/어느 주차 등)",
            "형식(파일/링크/문서 등) 또는 전달 방식이 제시된다",
            "필요 기한/시점과 감사 표현이 포함된다",
        ],
    ),

    # =========================================================
    # REQUEST_DEFAULT (기타 요청)
    # =========================================================
    DifficultyCard(
        id="request_default_beginner_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEFAULT,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 기타 요청(요청만 존재)",
        guide="무엇을 부탁하는지는 있으나, 배경/이유/조건이 부족한 단순 요청.",
        hint="요청 문장만 있고 맥락이 거의 없는 단계입니다.",
        checklist=[
            "무엇을 원하는지는 있으나 이유/배경이 없다",
            "상대가 판단할 조건(기간/범위 등)이 부족하다",
            "문장이 짧고 단순하다",
        ],
    ),
    DifficultyCard(
        id="request_default_intermediate_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEFAULT,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 배경/이유는 있으나 구체 조건 부족한 요청",
        guide="배경과 이유는 설명하지만, 원하는 결과/조건/기한이 덜 구체적인 경우.",
        hint="왜 부탁하는지는 알겠는데, 정확히 어떻게 해주면 되는지 덜 명확한 단계입니다.",
        checklist=[
            "배경/이유가 포함된다",
            "원하는 결과가 대략적으로 제시된다",
            "조건(기한/범위/우선순위)이 일부 부족하다",
        ],
    ),
    DifficultyCard(
        id="request_default_advanced_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEFAULT,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 조건/기한/배려가 정리된 기타 요청",
        guide="요청 내용, 배경, 원하는 결과, 조건/기한, 감사/배려 표현까지 포함된 요청.",
        hint="상대가 판단/처리하기 쉬운 정보 구조를 갖춘 완성형 요청입니다.",
        checklist=[
            "요청 내용과 원하는 결과가 명확하다",
            "조건(기한/범위/우선순위) 또는 대안이 제시된다",
            "정중한 마무리(감사/배려)가 포함된다",
        ],
    ),
]