"""공통 입력 파싱 유틸리티"""
"""개발자: https://github.com/Crispylux"""



from __future__ import annotations

from typing import List, Optional

MAX_PARTICIPANTS = 20
MIN_PARTICIPANTS = 2


def split_list(raw: str) -> List[str]:
    """콤마/공백이 섞인 입력을 정리된 리스트로 변환"""
    if raw is None:
        return []
    # 콤마와 개행을 공백으로 통일 후 split
    normalized = raw.replace("\n", ",").replace(" ", ",")
    items = [item.strip() for item in normalized.split(",")]
    return [item for item in items if item]


def validate_participants(participants: List[str]) -> Optional[str]:
    """문제가 있으면 에러 메시지를, 없으면 None을 반환"""
    if len(participants) < MIN_PARTICIPANTS:
        return f"참가자는 최소 {MIN_PARTICIPANTS}명 이상이어야 합니다. (쉼표로 구분해서 입력해주세요. 예: `쌀1,쌀2,쌀3`)"
    if len(participants) > MAX_PARTICIPANTS:
        return f"참가자는 최대 {MAX_PARTICIPANTS}명까지만 가능합니다. (현재: {len(participants)}명)"
    return None
