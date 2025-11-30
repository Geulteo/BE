import re
from typing import List, Optional, Dict, Any
from konlpy.tag import Okt

from models.keyword import KeywordRequest

okt = Okt()

# 핵심 품사 필터 (명사, 동사, 형용사)
TARGET_POS = ['Noun', 'Verb', 'Adjective']

# 입력 검증
def check_keyword_sufficiency(keywords: List[str]) -> Optional[str]:
    if len(keywords) < 2:
        return "키워드를 1~2개 더 적어주세요. (예시: 병원 / 내일 / 결석 / 과제 연장)"
    return None

# 전처리
def preprocess_text(raw_text: str) -> Dict[str, Any]:

    cleaned_text = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", raw_text) # 특수 문자 제거
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()  # 다중 공백 정리

    # 형태소 분석 + 핵심 품사 추출
    pos_result = okt.pos(cleaned_text, norm=True, stem=True)

    keywords = []
    pos_tags = []

    # (명사, 동사, 형용사)에 해당하는 단어만 추출
    for word, pos in pos_result:
        keywords.append(word)
        pos_tags.append(pos)

    # 키워드로 짧은 문장 생성 (SBERT 입력용)
    keyword_str = ", ".join(keywords)
    sentence_for_sbert = f"{keyword_str}와 관련된 상황입니다." if keywords else ""

    return {
        "cleaned_text": cleaned_text,
        "keywords": keywords,
        "pos_tags": pos_tags,
        "sentence_for_sbert": sentence_for_sbert,
    }

# 사용자 키워드 입력 처리
def process_user_input(data: KeywordRequest) -> Dict[str, Any]:

    # 전처리 실행
    preprocessed_data = preprocess_text(data.raw_text)
    keywords = preprocessed_data["keywords"]

    # 키워드 부족 검증
    insufficient_message = check_keyword_sufficiency(keywords)
    if insufficient_message:
        # 키워드가 부족 -> 안내 메시지 반환
        return {
            "error": True,
            "message": insufficient_message,
            "data": preprocessed_data,
        }

    # 최종 결과
    return {
        "error": False,
        "message": "전처리 및 검증 완료",
        "data": {
            **preprocessed_data,
            "tone": data.tone,
            "length_option": data.length_option,
            "target": data.target,
        }
    }