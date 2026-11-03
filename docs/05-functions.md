# 05. 함수

함수는 **자주 쓰는 코드 묶음에 이름을 붙인 것**입니다. 한 번 만들어 두면 이름만 불러서 여러 번 쓸 수 있습니다.

```python
def 함수이름(매개변수1, 매개변수2):
    """이 함수가 하는 일 (docstring)"""
    ...
    return 결과
```

- `def`로 정의하고, `함수이름(인자)`로 **호출**합니다.
- `return`은 결과를 돌려주고 함수를 끝냅니다. `return`이 없으면 `None`을 돌려줍니다.
- `print`는 화면에 보여 줄 뿐이고, `return`은 값을 호출한 쪽에 **넘겨 줍니다.** 둘은 다릅니다.

## 실행해 보기

```python title="examples/ch05_functions.py"
--8<-- "examples/ch05_functions.py"
```

## 매개변수의 종류

| 형태 | 예 | 설명 |
|---|---|---|
| 위치 인자 | `greet("민수")` | 순서대로 전달 |
| 키워드 인자 | `greet(name="민수")` | 이름으로 전달, 순서 무관 |
| 기본값 | `def greet(name, greeting="안녕하세요")` | 생략하면 기본값 사용 |
| `*args` | `def total(*numbers)` | 위치 인자 여러 개를 튜플로 |
| `**kwargs` | `def f(**options)` | 키워드 인자 여러 개를 딕셔너리로 |

!!! warning "기본값에 리스트를 쓰지 마세요"
    `def add(item, items=[])`처럼 쓰면 **같은 리스트가 호출마다 재사용**되어 값이 쌓입니다. `items=None`으로 받고 함수 안에서 `if items is None: items = []`로 만드세요.

## 변수의 범위(scope)

함수 안에서 만든 변수는 **함수 안에서만** 보입니다(지역 변수). 함수 밖의 값을 바꾸고 싶다면 `global`을 쓰기보다는 **값을 return해서 돌려받는 방식**을 권장합니다.

## lambda (이름 없는 짧은 함수)

```python
words = ["banana", "kiwi", "apple"]
print(sorted(words, key=lambda w: len(w)))   # ['kiwi', 'apple', 'banana']
```

## 연습문제

1. 숫자 리스트를 받아 평균을 돌려주는 `average(numbers)`를 만드세요. 빈 리스트면 `None`을 돌려줍니다.
2. 섭씨를 화씨로 바꾸는 `c_to_f(c)`를 만들고 0, 100, 36.5를 변환해 출력하세요. (F = C × 9/5 + 32)
3. 문자열과 횟수를 받아 반복한 문자열을 돌려주는 `repeat(text, times=2, sep=" ")`를 만드세요.

??? success "해답"
    ```python
    def average(numbers):
        if not numbers:
            return None
        return sum(numbers) / len(numbers)

    def c_to_f(c):
        return c * 9 / 5 + 32

    def repeat(text, times=2, sep=" "):
        return sep.join([text] * times)

    print(average([1, 2, 3]), average([]))      # 2.0 None
    for c in [0, 100, 36.5]:
        print(c, "->", c_to_f(c))               # 32.0, 212.0, 97.7
    print(repeat("야호", 3, sep="! "))           # 야호! 야호! 야호
    ```
