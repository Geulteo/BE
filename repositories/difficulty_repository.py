import json
from pathlib import Path
from typing import List

from models.difficulty_card import DifficultyCard


class DifficultyCardRepository:
    # 난이도 기준 카드(JSONL)를 로드하는 Repository
    def __init__(self, file_path: str = "./data/difficulty_cards.json"):
        self.file_path = Path(file_path)

    # JSON 배열 파일을 읽어서 DifficultyCard 모델 리스트로 변환
    def load_all(self) -> List[DifficultyCard]:

        # 파일 존재 여부 체크
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Difficulty card file not found: {self.file_path}"
            )

        try:
            # json.load() 사용
            with self.file_path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as e:
            # 파일 전체 JSON 파싱 오류를 명확하게 표시
            raise ValueError(
                f"Invalid JSON in difficulty_cards.json: {self.file_path}\nError: {e}"
            )

        # JSON 배열 필수 조건 명시
        if not isinstance(raw, list):
            raise ValueError(
                f"Difficulty card JSON must be an array of objects. Got: {type(raw)}"
            )

        cards: List[DifficultyCard] = []

        # 한 줄씩 파싱하던 로직 삭제 → 배열 순회 방식으로 변경
        for idx, item in enumerate(raw, start=1):
            try:
                cards.append(DifficultyCard(**item))
            except Exception as e:
                # 몇 번째 카드가 문제인지 명확하게 오류 표시
                raise ValueError(
                    f"Invalid card at index {idx} in difficulty_cards.json: {item}\nError: {e}"
                )

        return cards