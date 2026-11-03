# 클래스, dataclass, 타입 힌트
from __future__ import annotations

from dataclasses import dataclass, field


class BankAccount:
    """일반 클래스: __init__ 에서 속성을 만듭니다."""

    def __init__(self, owner: str, balance: int = 0) -> None:
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("입금액은 0보다 커야 합니다")
        self.balance += amount

    def __repr__(self) -> str:
        return f"BankAccount({self.owner!r}, {self.balance})"


acc = BankAccount("민수")
acc.deposit(1000)
print(acc, acc.balance)


class SavingsAccount(BankAccount):
    """상속: 부모 기능을 물려받고 일부를 바꿉니다."""

    def add_interest(self, rate: float) -> None:
        self.balance += int(self.balance * rate)


sav = SavingsAccount("지은", 10000)
sav.add_interest(0.05)
print(sav)


@dataclass
class Article:
    """dataclass: __init__, __repr__, __eq__ 를 자동으로 만들어 줍니다."""

    title: str
    url: str
    tags: list[str] = field(default_factory=list)   # 가변 기본값은 이렇게
    views: int = 0


a = Article("파이썬 입문", "https://example.com/1", ["python"])
b = Article("파이썬 입문", "https://example.com/1", ["python"])
print(a)
print("같은 값인가요?", a == b)


def top_articles(items: list[Article], n: int = 3) -> list[str]:
    """타입 힌트는 실행에 영향을 주지 않지만, 읽는 사람과 편집기에 큰 도움이 됩니다."""
    return [x.title for x in sorted(items, key=lambda x: x.views, reverse=True)[:n]]


print(top_articles([Article("A", "u", views=5), Article("B", "u", views=9)]))
