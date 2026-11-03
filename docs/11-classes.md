# 11. 클래스·dataclass·타입 힌트

## 클래스는 "설계도", 객체는 "만들어진 물건"

관련된 **데이터(속성)**와 **동작(메서드)**을 하나로 묶을 때 클래스를 씁니다.

```python
class Dog:
    def __init__(self, name):     # 객체를 만들 때 자동 호출 (생성자)
        self.name = name          # self = 지금 만들어지는 그 객체

    def bark(self):               # 메서드: 첫 매개변수는 항상 self
        return f"{self.name}: 멍멍"

d = Dog("바둑이")                 # 객체(인스턴스) 생성
print(d.bark())                   # 바둑이: 멍멍
```

## 실행해 보기

```python title="examples/ch11_classes.py"
--8<-- "examples/ch11_classes.py"
```

## 상속

`class SavingsAccount(BankAccount):`처럼 쓰면 부모 클래스의 속성과 메서드를 물려받습니다. 부모 메서드를 그대로 쓰면서 일부만 바꾸거나 추가할 수 있습니다. 부모의 메서드를 부를 때는 `super().메서드()`를 씁니다.

## 특별한 메서드 (던더 메서드)

이름 앞뒤에 밑줄 두 개가 붙은 메서드는 파이썬이 특별한 때 자동으로 부릅니다.

| 메서드 | 언제 호출되나 |
|---|---|
| `__init__` | 객체를 만들 때 |
| `__repr__` | `print`나 대화형 모드에서 객체를 보여 줄 때 |
| `__eq__` | `==`로 비교할 때 |
| `__len__` | `len(객체)` |

## dataclass

데이터를 담는 용도의 클래스라면 `@dataclass`를 붙이세요. `__init__`, `__repr__`, `__eq__`를 **자동으로** 만들어 줍니다.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int = 0

print(Point(1, 2))           # Point(x=1, y=2)
print(Point(1) == Point(1))  # True
```

- 리스트·딕셔너리 같은 **바뀔 수 있는 기본값**은 `field(default_factory=list)`로 지정합니다.
- `@dataclass(frozen=True)`로 만들면 값을 바꿀 수 없는 객체가 됩니다.
- `dataclasses.asdict(obj)`로 딕셔너리로 바꿔 JSON으로 저장하기 쉽습니다.

## 타입 힌트

```python
def add(a: int, b: int) -> int:
    return a + b

names: list[str] = []
config: dict[str, int] = {}
maybe: str | None = None      # str 또는 None (Python 3.10+)
```

- 타입 힌트는 **실행에 영향을 주지 않습니다.** `add("a", "b")`도 그냥 실행됩니다.
- 대신 VS Code 같은 편집기가 자동 완성과 오류 경고를 해 주고, 코드를 읽는 사람이 이해하기 쉬워집니다.
- `mypy` 같은 도구로 타입 오류를 미리 검사할 수도 있습니다.
- `list[str]`, `str | None` 문법은 각각 Python 3.9, 3.10부터 지원합니다. 파일 맨 위에 `from __future__ import annotations`를 두면 더 낮은 버전에서도 힌트로는 쓸 수 있습니다.

## 연습문제

1. `Rectangle` 클래스를 만들고 `area()`, `perimeter()` 메서드를 구현하세요.
2. 할 일 하나를 나타내는 dataclass `Todo(title: str, done: bool = False)`를 만들고, 리스트에서 완료되지 않은 항목의 제목만 뽑으세요.
3. `BankAccount`에 `withdraw(amount)`를 추가하고, 잔액보다 많이 빼려 하면 `ValueError`를 일으키세요.

??? success "해답"
    ```python
    from dataclasses import dataclass

    class Rectangle:
        def __init__(self, width: float, height: float) -> None:
            self.width = width
            self.height = height

        def area(self) -> float:
            return self.width * self.height

        def perimeter(self) -> float:
            return 2 * (self.width + self.height)

    r = Rectangle(3, 4)
    print(r.area(), r.perimeter())   # 12 14

    @dataclass
    class Todo:
        title: str
        done: bool = False

    todos = [Todo("장보기"), Todo("운동", done=True), Todo("공부")]
    print([t.title for t in todos if not t.done])   # ['장보기', '공부']

    class BankAccount:
        def __init__(self, owner: str, balance: int = 0) -> None:
            self.owner = owner
            self.balance = balance

        def withdraw(self, amount: int) -> None:
            if amount > self.balance:
                raise ValueError("잔액이 부족합니다")
            self.balance -= amount

    acc = BankAccount("민수", 1000)
    acc.withdraw(300)
    print(acc.balance)   # 700
    ```
