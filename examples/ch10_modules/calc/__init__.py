"""calc 패키지: 간단한 계산 함수 모음"""
from .ops import add, multiply   # 상대 import: 같은 패키지 안의 ops 모듈

__all__ = ["add", "multiply"]
