"""
세션 메모리 관리

훈련 세션의 히스토리를 메모리에 저장/조회하여
이전 시도를 기억하고 개선 피드백을 제공
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from threading import Lock


class SessionMemory:

    def __init__(self, default_expiry_minutes: int = 30):
        self.sessions: Dict[str, List[Dict]] = {}
        self.session_expiry: Dict[str, datetime] = {}
        self.default_expiry_minutes = default_expiry_minutes
        self.lock = Lock() 

    def add_turn(self, session_id: str, turn_data: Dict) -> None:
        with self.lock:
            # 세션이 없으면 생성
            if session_id not in self.sessions:
                self.sessions[session_id] = []

            # Turn 데이터 추가
            self.sessions[session_id].append(turn_data)

            # 세션 만료 시간 갱신 
            expiry_time = datetime.now() + timedelta(minutes=self.default_expiry_minutes)
            self.session_expiry[session_id] = expiry_time

    def get_history(self, session_id: str, last_n: int = 3) -> List[Dict]:
        with self.lock:
            if session_id not in self.sessions:
                return []

            # 만료된 세션인지 확인
            if self._is_expired(session_id):
                self._remove_session(session_id)
                return []

            # 최근 N개 반환
            return self.sessions[session_id][-last_n:]

    def get_turn_count(self, session_id: str) -> int:
        with self.lock:
            if session_id not in self.sessions:
                return 0

            if self._is_expired(session_id):
                self._remove_session(session_id)
                return 0

            return len(self.sessions[session_id])

    def clear_session(self, session_id: str) -> bool:
        with self.lock:
            if session_id in self.sessions:
                self._remove_session(session_id)
                return True
            return False

    def clear_expired_sessions(self) -> int:
        with self.lock:
            now = datetime.now()
            expired = [
                sid for sid, exp_time in self.session_expiry.items()
                if exp_time < now
            ]

            for sid in expired:
                self._remove_session(sid)

            return len(expired)

    def get_all_sessions_count(self) -> int:
        with self.lock:
            return len(self.sessions)

    def session_exists(self, session_id: str) -> bool:
        with self.lock:
            if session_id not in self.sessions:
                return False

            if self._is_expired(session_id):
                self._remove_session(session_id)
                return False

            return True

    def _is_expired(self, session_id: str) -> bool:
        if session_id not in self.session_expiry:
            return True

        return datetime.now() > self.session_expiry[session_id]

    def _remove_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_expiry:
            del self.session_expiry[session_id]


# 전역 메모리 인스턴스 (FastAPI 앱 전체에서 공유)
session_memory = SessionMemory(default_expiry_minutes=30)

def get_session_memory() -> SessionMemory:
    return session_memory


def cleanup_expired_sessions() -> int:
    return session_memory.clear_expired_sessions()
