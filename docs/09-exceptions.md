# 09. 예외 처리

프로그램 실행 중 문제가 생기면 파이썬은 **예외(exception)**를 일으키고, 아무도 처리하지 않으면 프로그램이 멈추며 **트레이스백(traceback)**을 출력합니다.

## 트레이스백 읽는 법

```text
Traceback (most recent call last):
  File "D:\study\app.py", line 3, in <module>
    print(10 / count)
          ~~~^~~~~~~
ZeroDivisionError: division by zero
```

**맨 아래 줄부터** 읽으세요. `ZeroDivisionError`(예외 종류)와 메시지가 무엇이 잘못됐는지, 그 위의 `File ..., line 3`이 어디서 일어났는지 알려 줍니다.

## try / except / else / finally

```python
try:
    위험할 수 있는 코드
except 예외종류 as e:
    그 예외가 났을 때 할 일
else:
    예외가 없을 때 할 일
finally:
    예외가 나든 안 나든 항상 할 일 (정리 작업)
```

## 실행해 보기

```python title="examples/ch09_exceptions.py"
--8<-- "examples/ch09_exceptions.py"
```

## 자주 만나는 예외

| 예외 | 언제 |
|---|---|
| `ValueError` | 값의 형태가 잘못됨 (`int("abc")`) |
| `TypeError` | 자료형이 맞지 않음 (`"a" + 1`) |
| `KeyError` | 딕셔너리에 없는 키 |
| `IndexError` | 리스트 범위를 벗어난 번호 |
| `FileNotFoundError` | 파일이 없음 (현재 폴더 확인!) |
| `ZeroDivisionError` | 0으로 나눔 |
| `ModuleNotFoundError` | import할 모듈을 못 찾음 ([10장](10-modules.md)) |

더 많은 사례는 [부록: 자주 만나는 오류](appendix-errors.md)에 모았습니다.

## 좋은 예외 처리 습관

- **필요한 예외만** 구체적으로 잡으세요. `except:`나 `except Exception:`으로 모두 삼키면 진짜 버그를 놓칩니다.
- 예외를 잡았다면 **무슨 일이 있었는지 알 수 있게** 메시지를 남기세요.
- 오류 메시지·로그에 **비밀번호나 API 키 같은 시크릿이 섞이지 않도록** 주의하세요. ([15장](15-email-env.md))
- 직접 만든 함수에서 잘못된 입력을 받으면 `raise ValueError("이유")`로 알리세요.

## 연습문제

1. 문자열 리스트 `["10", "x", "3", ""]`를 정수로 바꾸되, 바꿀 수 없는 값은 건너뛰고 합계를 구하세요.
2. 딕셔너리에서 키를 찾는 `safe_get(d, key)`를 `try/except KeyError`로 만들고, 없으면 `"(없음)"`을 돌려주세요.

??? success "해답"
    ```python
    total = 0
    for text in ["10", "x", "3", ""]:
        try:
            total += int(text)
        except ValueError:
            print(f"건너뜀: {text!r}")
    print("합계:", total)   # 13

    def safe_get(d, key):
        try:
            return d[key]
        except KeyError:
            return "(없음)"

    print(safe_get({"a": 1}, "a"), safe_get({"a": 1}, "b"))   # 1 (없음)
    ```
