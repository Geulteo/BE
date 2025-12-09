from __future__ import annotations

from typing import Dict, List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI

from config.settings import get_settings
from core.type_enums import IntentType

settings = get_settings()

llm_client = OpenAI(api_key=settings.OPENAI_API_KEY)

# 0) Rule-based 키워드 감지 점수

INTENT_KEYWORD_BOOST = {
    IntentType.REQUEST: ["부탁", "가능", "연장", "도움", "요청", "양해"],
    IntentType.QUESTION: ["무엇", "왜", "어떻게", "알다", "궁금", "확인"],
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

# Utility: 문장 여부 판단
def is_full_sentence(text: str, keyword_count: Optional[int] = None) -> bool:
    text = text.strip()
    if not text:
        return False
    if len(text) <= 6:
        return False
    space_count = text.count(" ")

    verb_like = ["다", "합니다", "했습니다", "해요", "했어요", "싶다"]
    if any(text.endswith(v) for v in verb_like):
        return True

    if space_count >= 2:
        return True

    if any(j in text for j in ["은","는","이","가","을","를"]) and space_count >= 1:
        return True

    return False

# 1) 템플릿 구성
INTENT_TEMPLATES: Dict[IntentType, List[str]] = {
    IntentType.REQUEST: [
        "죄송하지만 도움을 요청드리고 싶습니다.",
        "이 부분에 대해 조금만 더 설명해주실 수 있을까요?",
        "시간 괜찮으시면 잠시 상담 가능하실까요?",
        "자료를 다시 한 번 보내주실 수 있을까요?",
        "일정 조정이 가능하신지 여쭤보고 싶습니다.",
        "시간 괜찮으시면 의견을 여쭙고 싶습니다.",
        "파일을 수정해서 다시 제출해도 괜찮을까요?",
        "다음 주에 면담 시간을 잡아주실 수 있을까요?",
        "급하게 확인이 필요해서 검토 부탁드립니다.",
        "제가 이해하지 못한 부분을 알려주실 수 있을까요?",
    ],
    IntentType.QUESTION: [
        "이 문제가 발생한 원인이 무엇인가요?",
        "파일이 열리지 않는 이유를 알 수 있을까요?",
        "제가 맡은 역할이 정확히 무엇인가요?",
        "이 부분을 어떻게 해결해야 하나요?",
        "이 단계 이후의 절차가 무엇인가요?",
        "이 내용이 맞는지 확인해주실 수 있나요?",
        "왜 이런 오류가 발생하는지 설명해주실 수 있을까요?",
        "이 기능은 어떤 방식으로 사용하는 건가요?",
        "다음 일정은 어떻게 확인할 수 있나요?",
        "이 항목이 의미하는 바가 무엇인가요?",
    ],
    IntentType.NOTICE: [
        "오늘 예정된 실험은 사정으로 인해 취소되었습니다.",
        "다음 회의는 일정 변경으로 연기됩니다.",
        "업데이트된 과제 파일이 업로드되었습니다.",
        "주의사항이 변경되었으니 다시 확인해주세요.",
        "수업 장소가 101호에서 103호로 변경됩니다.",
        "중요한 안내 사항이 있어 공유드립니다.",
        "일정이 조정되었음을 알려드립니다.",
        "새로운 자료가 추가되었으니 확인 부탁드립니다.",
        "공지된 일정에 일부 변동이 있습니다.",
        "발표 순서가 확정되어 안내드립니다.",
    ],
    IntentType.APOLOGY: [
        "제가 실수하여 불편을 드린 점 진심으로 사과드립니다.",
        "제 행동으로 인해 불편을 끼쳐 정말 죄송합니다.",
        "약속을 지키지 못해 죄송합니다.",
        "제 부주의로 문제가 발생해 죄송합니다.",
        "혼동을 드린 점 사과드립니다.",
        "늦게 응답드려 죄송합니다.",
        "제 전달이 정확하지 않아 죄송합니다.",
        "기대에 미치지 못한 점 사과드립니다.",
        "오해를 일으켜 죄송합니다.",
        "제가 처리하지 못해 죄송합니다.",
    ],
    IntentType.COMPLAINT: [
        "문의드린 지 오래되었지만 아직 답변을 받지 못했습니다.",
        "공지 내용이 명확하지 않아 혼란을 겪고 있습니다.",
        "자료가 자꾸 오류가 나서 불편합니다.",
        "서비스 처리 속도가 너무 느립니다.",
        "제공된 안내와 실제 내용이 일치하지 않습니다.",
        "여러 차례 문의했으나 답변이 없어 불편합니다.",
        "시스템 오류가 반복적으로 발생하고 있습니다.",
        "업데이트 이후 기능이 정상 작동하지 않습니다.",
        "문제가 해결되지 않아 난처합니다.",
        "프로세스가 너무 복잡해 불편함을 느낍니다.",
    ],
}

# 2) 키워드 → 문장 복원 (Intent 추론 포함)
def restore_sentence_from_keywords(keywords: List[str]) -> str:

    prompt = f"""
당신은 사용자의 의도를 추론하는 보조 도구입니다.

다음 키워드를 보고, 사용자가 표현하려는 의도가
Request / Question / Notice / Apology / Complaint 중 무엇일지 먼저 유추하세요.

그 후, 그 의도(Intent)에 맞는 자연스러운 한국어 문장을 생성하세요.

키워드: {", ".join(keywords)}

조건:
- 키워드 의미를 반드시 반영할 것
- 가장 자연스럽고 의미가 잘 드러나는 문장 1개 생성
- Intent가 드러나는 문체로 작성할 것
- 문장만 출력
"""

    res = llm_client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=50,
    )

    return res.choices[0].message.content.strip()


# 3) Intent Classifier

class IntentClassifier:

    def __init__(self, model: SentenceTransformer | None = None, top_k: int = 3):
        self.model = model or SentenceTransformer(settings.SBERT_MODEL_NAME)
        self.top_k = top_k

        self.template_texts, self.template_labels = [], []

        for intent, examples in INTENT_TEMPLATES.items():
            for s in examples:
                self.template_texts.append(s)
                self.template_labels.append(intent)

        self.template_embeddings = self.model.encode(
            self.template_texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    # SBERT 기반 Top-K 점수 계산
    def _compute_scores_top_k(self, sentence: str) -> Dict[IntentType, float]:

        q = self.model.encode(sentence, convert_to_numpy=True, normalize_embeddings=True)
        sims = self.template_embeddings @ q

        grouped = {intent: [] for intent in INTENT_TEMPLATES.keys()}
        for idx, sim in enumerate(sims):
            grouped[self.template_labels[idx]].append(float(sim))

        scores = {}
        for intent, vals in grouped.items():
            scores[intent] = float(np.mean(sorted(vals, reverse=True)[: self.top_k]))

        return scores

    # Rule-based 보정값 계산
    def _boost_from_keywords(self, keywords: List[str]) -> Dict[IntentType, float]:
        boost = {intent: 0.0 for intent in INTENT_TEMPLATES}
        if not keywords:
            return boost

        for intent, kw_list in INTENT_KEYWORD_BOOST.items():
            if any(k in " ".join(keywords) for k in kw_list):
                boost[intent] += INTENT_KEYWORD_WEIGHT[intent]

        return boost

    # 최종 예측
    def predict(
        self,
        raw_text: str,
        keywords: List[str] | None = None,
        top_threshold: float = 0.40,
        diff_threshold: float = 0.06,
    ) -> Dict:

        raw_text = (raw_text or "").strip()
        keyword_count = len(keywords) if keywords else None

        # 입력 타입 판정
        if is_full_sentence(raw_text, keyword_count):
            sentence_for_sbert = raw_text
        else:
            sentence_for_sbert = restore_sentence_from_keywords(keywords or [])

        # SBERT 점수 계산
        sbert_scores = self._compute_scores_top_k(sentence_for_sbert)

        # rule-based boost 계산
        boost_scores = self._boost_from_keywords(keywords or [])

        # SBERT + rule score 합산
        final_scores = {intent: sbert_scores[intent] + boost_scores[intent]
                        for intent in sbert_scores}

        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, top_score = ranked[0]
        second_score = ranked[1][1]

        need_more_info = (top_score < top_threshold) or \
                         ((top_score - second_score) < diff_threshold)

        return {
            "sentence_used": sentence_for_sbert,
            "predicted_intent": top_intent.value,
            "scores": {k.value: float(v) for k, v in final_scores.items()},
            "top_score": float(top_score),
            "second_score": float(second_score),
            "need_more_info": need_more_info,
            "need_more_info_message":
                ("의미가 애매합니다. 좀 더 구체적으로 입력해주세요."
                 if need_more_info else None),
        }
