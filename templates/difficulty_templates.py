from __future__ import annotations
from typing import List

from models.difficulty_card import DifficultyCard
from core.type_enums import IntentType, TemplateId
from core.level_enums import DifficultyLevel


DIFFICULTY_CARDS: List[DifficultyCard] = [
    # =========================================================
    # REQUEST  (슬롯: 상황 / 이유 / 요청 / 마무리)
    # =========================================================
    DifficultyCard(
        id="request_beginner_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEFAULT,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 기본 요청(정보 부족)",
        guide="요청은 있지만 상황/이유/조건 정보가 부족해 상대가 판단하기 어려운 경우.",
        hint="요청 의도는 전달되지만 핵심 정보(무엇/언제/왜/어떻게)가 빠져 있습니다.",
        checklist=[
            "요청만 있고 상황/배경 설명이 거의 없다",
            "이유가 없거나 매우 짧다",
            "조건(기한/범위/대상/원하는 결과)이 불명확하다",
        ],
    ),
    DifficultyCard(
        id="request_intermediate_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEFAULT,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 이유 포함 요청(조건 일부 부족)",
        guide="상황과 이유는 말하지만, 기한/대안/구체 조건이 일부 부족한 경우.",
        hint="상대가 이해는 하지만 처리 기준이 부족해 추가 질문이 필요할 수 있습니다.",
        checklist=[
            "상황과 요청이 연결되어 설명된다",
            "구체적인 이유가 포함된다(예: 일정/개인 사정)",
            "조건(기한/범위/우선순위/대안) 중 일부가 부족하다",
        ],
    ),
    DifficultyCard(
        id="request_advanced_1",
        intent=IntentType.REQUEST,
        template_id=TemplateId.REQUEST_DEFAULT,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 조건/대안/배려까지 갖춘 요청",
        guide="상황·이유·요청·마무리가 자연스럽고, 상대가 바로 처리할 수 있을 정도로 구체적인 경우.",
        hint="요청 내용과 조건이 명확하고, 배려/감사 표현까지 포함된 완성형입니다.",
        checklist=[
            "상황-이유-요청이 논리적으로 정리되어 있다",
            "원하는 결과/조건(기한·범위·형식 등)이 구체적이다",
            "대안 또는 배려/감사 표현이 포함된다",
        ],
    ),

    # =========================================================
    # QUESTION (슬롯: 상황 / 모르겠는 점 / 구체적 질문)
    # =========================================================
    DifficultyCard(
        id="question_beginner_1",
        intent=IntentType.QUESTION,
        template_id=TemplateId.QUESTION_DEFAULT,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 단순 질문(맥락 부족)",
        guide="무엇이 궁금한지는 있으나 배경/전제/시도한 내용이 부족한 경우.",
        hint="질문은 했지만 상대가 어떤 상황인지 파악하기 어렵습니다.",
        checklist=[
            "질문만 있고 상황/전제가 부족하다",
            "‘뭐가 문제인지’가 뭉뚱그려져 있다",
            "시도한 내용/현재 상태가 없다",
        ],
    ),
    DifficultyCard(
        id="question_intermediate_1",
        intent=IntentType.QUESTION,
        template_id=TemplateId.QUESTION_DEFAULT,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 배경 포함 질문(범위/조건 일부 부족)",
        guide="상황과 궁금한 점은 설명하지만, 질문의 범위/조건/원하는 답 형태가 덜 명확한 경우.",
        hint="상대가 답할 수는 있으나 추가 확인이 필요한 질문입니다.",
        checklist=[
            "상황/배경(무엇을 하다가)이 포함된다",
            "모르겠는 점이 비교적 구체적이다",
            "질문 범위/조건(예: 버전/환경/기준)이 일부 부족하다",
        ],
    ),
    DifficultyCard(
        id="question_advanced_1",
        intent=IntentType.QUESTION,
        template_id=TemplateId.QUESTION_DEFAULT,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 조건/시도/원하는 답까지 명확한 질문",
        guide="배경, 문제 지점, 시도한 내용, 원하는 답변 형태까지 갖춰 답변 효율이 높은 경우.",
        hint="상대가 바로 핵심을 짚어 답할 수 있는 완성형 질문입니다.",
        checklist=[
            "상황/전제와 문제 지점이 명확하다",
            "시도한 내용/현재 상태가 정리되어 있다",
            "원하는 답(절차/기준/예시 등)이 구체적이다",
        ],
    ),

    # =========================================================
    # NOTICE (슬롯: 배경 / 핵심 정보 / 변경사항 / 마무리)
    # =========================================================
    DifficultyCard(
        id="notice_beginner_1",
        intent=IntentType.NOTICE,
        template_id=TemplateId.NOTICE_GENERAL,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 공지(핵심 정보 부족)",
        guide="공지하려는 의도는 있으나 일정/장소/대상/변경사항 등 핵심 정보가 빠진 경우.",
        hint="무슨 공지인지 감은 오지만, 실행에 필요한 정보가 부족합니다.",
        checklist=[
            "무엇이 공지인지 핵심이 모호하다",
            "대상/일정/장소/방법 등 필수 정보가 빠진다",
            "변경사항 또는 해야 할 행동이 명확하지 않다",
        ],
    ),
    DifficultyCard(
        id="notice_intermediate_1",
        intent=IntentType.NOTICE,
        template_id=TemplateId.NOTICE_GENERAL,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 공지(주요 정보 포함, 일부 불명확)",
        guide="배경과 핵심 정보는 있으나 변경 전/후 비교, 세부 행동 지침이 부족한 경우.",
        hint="필수 정보는 대체로 있지만, 수신자가 헷갈릴 수 있는 부분이 남아 있습니다.",
        checklist=[
            "배경 또는 목적이 간단히 설명된다",
            "일정/장소/대상 등 주요 정보가 포함된다",
            "변경 전/후 또는 후속 행동 안내가 일부 부족하다",
        ],
    ),
    DifficultyCard(
        id="notice_advanced_1",
        intent=IntentType.NOTICE,
        template_id=TemplateId.NOTICE_GENERAL,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 공지(변경사항/행동지침까지 명확)",
        guide="배경-핵심정보-변경사항-마무리가 깔끔하고, 수신자가 바로 행동할 수 있는 경우.",
        hint="혼동 없이 전달되는 완성형 공지입니다.",
        checklist=[
            "핵심 정보(무엇/언제/어디/대상)가 명확하다",
            "변경사항(전/후)과 이유/영향이 정리되어 있다",
            "수신자가 해야 할 행동/문의 방법이 포함된다",
        ],
    ),

    # =========================================================
    # COMPLAINT (슬롯: 문제 상황 / 영향 / 해결 요청)
    # =========================================================
    DifficultyCard(
        id="complaint_beginner_1",
        intent=IntentType.COMPLAINT,
        template_id=TemplateId.COMPLAINT_DEFAULT,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 불만 제기(상황 설명 부족)",
        guide="불만 감정만 강하고, 언제/어디서/무엇이 문제였는지 구체 정보가 부족한 경우.",
        hint="문제는 있는 듯하지만 재현/확인이 어려운 단계입니다.",
        checklist=[
            "문제 상황이 추상적이고 구체성이 부족하다",
            "발생 시점/환경/조건 정보가 없다",
            "원하는 해결(요청 사항)이 불명확하다",
        ],
    ),
    DifficultyCard(
        id="complaint_intermediate_1",
        intent=IntentType.COMPLAINT,
        template_id=TemplateId.COMPLAINT_DEFAULT,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 불만 제기(상황/영향 포함, 요청 일부 부족)",
        guide="문제 상황과 영향은 설명하지만, 원하는 해결 방식이나 증빙 정보가 부족한 경우.",
        hint="상대가 대응 가능하지만 추가 정보가 필요할 수 있습니다.",
        checklist=[
            "문제 상황(무엇이 잘못됐는지)이 설명된다",
            "영향(불편/손해/지연)이 언급된다",
            "원하는 해결 요청이 있으나 구체 조건/증빙이 부족하다",
        ],
    ),
    DifficultyCard(
        id="complaint_advanced_1",
        intent=IntentType.COMPLAINT,
        template_id=TemplateId.COMPLAINT_DEFAULT,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 재현조건/증빙/해결요청이 명확한 불만",
        guide="문제 상황, 재현 조건, 영향, 원하는 해결을 정중하게 구조화한 경우.",
        hint="상대가 즉시 조치하기 쉬운 완성형 문제 제기입니다.",
        checklist=[
            "발생 시점/환경/재현 조건이 구체적이다",
            "영향과 우선순위가 명확하다",
            "원하는 해결(환불/조치/가이드)과 증빙(로그/캡처)이 제시된다",
        ],
    ),

    # =========================================================
    # APOLOGY (슬롯: 상황 / 원인 / 사과 / 후속 조치)
    # =========================================================
    DifficultyCard(
        id="apology_beginner_1",
        intent=IntentType.APOLOGY,
        template_id=TemplateId.APOLOGY_DEFAULT,
        level=DifficultyLevel.BEGINNER,
        title="초급 - 단순 사과(원인/후속 조치 부족)",
        guide="미안하다는 표현은 있으나 무엇에 대한 사과인지/어떻게 할지 정보가 부족한 경우.",
        hint="감정 표현은 있지만 상대의 불편을 해소하기엔 부족합니다.",
        checklist=[
            "사과 표현만 있고 상황 설명이 부족하다",
            "원인 또는 책임 인식이 약하다",
            "후속 조치/재발 방지 언급이 없다",
        ],
    ),
    DifficultyCard(
        id="apology_intermediate_1",
        intent=IntentType.APOLOGY,
        template_id=TemplateId.APOLOGY_DEFAULT,
        level=DifficultyLevel.INTERMEDIATE,
        title="중급 - 상황/원인 포함 사과(조치 일부 부족)",
        guide="무슨 일이 있었는지와 원인은 설명하지만, 구체적인 해결 일정/방법이 부족한 경우.",
        hint="상대가 납득은 가능하지만, 신뢰 회복을 위한 조치가 더 필요합니다.",
        checklist=[
            "상황(무슨 일이 있었는지)이 설명된다",
            "원인/책임 인식이 포함된다",
            "후속 조치가 있으나 구체성(언제/어떻게)이 부족하다",
        ],
    ),
    DifficultyCard(
        id="apology_advanced_1",
        intent=IntentType.APOLOGY,
        template_id=TemplateId.APOLOGY_DEFAULT,
        level=DifficultyLevel.ADVANCED,
        title="고급 - 해결계획/재발방지까지 포함한 사과",
        guide="상황-원인-사과-후속조치가 구조적으로 정리되어 신뢰 회복에 도움이 되는 경우.",
        hint="구체적인 조치와 재발 방지가 포함된 완성형 사과입니다.",
        checklist=[
            "상황/원인이 명확하고 변명 없이 정리되어 있다",
            "구체적인 후속 조치(일정/방법/담당)가 포함된다",
            "재발 방지 약속과 정중한 마무리가 포함된다",
        ],
    ),
]