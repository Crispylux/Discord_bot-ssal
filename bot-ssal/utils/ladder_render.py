"""
사다리타기(Ghost Leg / Amidakuji) 로직 - 텍스트 결과 추출
"""
"""개발자: https://github.com/Crispylux"""


from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class LadderResult:
    """사다리타기 1회 실행 결과"""
    participants: List[str]
    results: List[str]
    # mapping[i] = participants[i] 가 도착하는 results의 인덱스
    mapping: List[int]

    def pairs(self) -> List[Tuple[str, str]]:
        return [(self.participants[i], self.results[self.mapping[i]]) for i in range(len(self.participants))]


def _generate_rungs(n_cols: int, n_rows: int) -> List[List[bool]]:
    rungs = [[False] * (n_cols - 1) for _ in range(n_rows)]
    if n_cols < 2:
        return rungs

    for row in range(n_rows):
        col = 0
        while col < n_cols - 1:
            # 대략 40~55% 확률로 가로줄 생성
            if random.random() < 0.45:
                rungs[row][col] = True
                col += 2  # 바로 옆 칸은 건너뛰어 겹침 방지
            else:
                col += 1

    # 완전히 가로줄이 하나도 없는 사다리는 재미없으니 최소 1개는 보장
    if n_cols >= 2 and not any(any(r) for r in rungs):
        row = random.randrange(n_rows)
        rungs[row][random.randrange(n_cols - 1)] = True

    return rungs


def run_ladder(participants: List[str], results: List[str], n_rows: int | None = None) -> LadderResult:
    n = len(participants)
    if n_rows is None:
        n_rows = max(8, min(20, n * 3))

    rungs = _generate_rungs(n, n_rows)

    mapping = [0] * n
    for start in range(n):
        col = start
        for row in rungs:
            if col < len(row) and row[col]:
                col += 1
            elif col - 1 >= 0 and row[col - 1]:
                col -= 1
        mapping[start] = col

    return LadderResult(participants=participants, results=results, mapping=mapping)
