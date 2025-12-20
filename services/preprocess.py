import re
from typing import List, Optional, Dict, Any
from konlpy.tag import Okt
from models.keyword import KeywordRequest

okt = None

def _get_okt():
    global okt
    if okt is None:
        okt = Okt()
    return okt

# 키워드 개수가 충분한지 검증
def check_keyword_sufficiency(keywords: List[str]) -> Optional[str]:
    if len(keywords) < 2:
        return "키워드를 1~2개 더 적어주세요. (예시: 병원 / 내일 / 결석 / 과제 연장)"
    return None

# 형태소 분석 및 품사 태그 추출
def _extract_pos_tags(text: str) -> tuple[List[str], List[str]]:
    okt_instance = _get_okt()
    pos_result = okt_instance.pos(text, norm=True, stem=True)
    keywords = [word for word, pos in pos_result]
    pos_tags = [pos for word, pos in pos_result]
    return keywords, pos_tags

# SBERT 임베딩용 문장 생성
def _generate_sbert_sentence(keywords: List[str]) -> str:
    keyword_str = ", ".join(keywords)
    return f"{keyword_str}와 관련된 상황입니다." if keywords else ""

# 사용자의 텍스트를 전처리 및 키워드 개수를 검증
def preprocess_and_validate_input(data: KeywordRequest) -> Dict[str, Any]:

    cleaned_text = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", data.raw_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    # 형태소 분석 및 키워드 추출
    keywords, pos_tags = _extract_pos_tags(cleaned_text)
    sentence_for_sbert = _generate_sbert_sentence(keywords)

    # 기본 데이터 구조
    preprocessed_data = {
        "cleaned_text": cleaned_text,
        "keywords": keywords,
        "pos_tags": pos_tags,
        "sentence_for_sbert": sentence_for_sbert,
        "tone": data.tone,
        "length_option": data.length_option,
        "target": data.target
    }

    # 키워드 부족 검증 및 응답 분기
    insufficient_message = check_keyword_sufficiency(keywords)

    if insufficient_message:
        # 오류 발생 시 오류 플래그와 메시지를 dict에 추가하여 반환
        return {
            "error": True,
            "message": insufficient_message,
            **preprocessed_data
        }

    # 정상적인 경우
    return {
        "error": False,
        "message": "전처리 및 검증 완료",
        **preprocessed_data
    }

def build_sentence_for_sbert(raw_text: str) -> str:
    cleaned_text = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", raw_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    keywords, _ = _extract_pos_tags(cleaned_text)
    return _generate_sbert_sentence(keywords)