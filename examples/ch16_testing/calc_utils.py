"""테스트 대상 함수들"""


def average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("빈 목록의 평균은 구할 수 없습니다")
    return sum(numbers) / len(numbers)


def normalize_email(text: str) -> str:
    """앞뒤 공백을 지우고 소문자로 바꿉니다. '@' 가 없으면 ValueError."""
    email = text.strip().lower()
    if "@" not in email:
        raise ValueError(f"메일 주소 형식이 아닙니다: {text!r}")
    return email
