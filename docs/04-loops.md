# 04. 반복문

같은 일을 여러 번 할 때 반복문을 씁니다.

- **`for`**: 리스트·문자열·`range` 같은 묶음에서 값을 **하나씩 꺼내며** 반복
- **`while`**: 조건이 **참인 동안** 반복

## for와 range

```python
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)
```

| 형태 | 만들어지는 값 |
|---|---|
| `range(5)` | 0 1 2 3 4 |
| `range(1, 6)` | 1 2 3 4 5 (끝 값 6은 **포함하지 않음**) |
| `range(0, 10, 3)` | 0 3 6 9 (3씩 증가) |
| `range(5, 0, -1)` | 5 4 3 2 1 |

## 실행해 보기

```python title="examples/ch04_loops.py"
--8<-- "examples/ch04_loops.py"
```

## break와 continue

- `break`: 반복을 **즉시 끝냅니다.**
- `continue`: 이번 차례의 나머지를 **건너뛰고** 다음 차례로 갑니다.

!!! danger "무한 반복 주의"
    `while` 조건이 계속 참이면 프로그램이 끝나지 않습니다. 멈추려면 PowerShell에서 ++ctrl+c++를 누르세요. 반복 안에서 조건을 바꾸는 코드(`count -= 1` 등)를 빠뜨리지 않았는지 확인하세요.

## 중첩 반복

```python
for dan in range(2, 4):
    for n in range(1, 4):
        print(f"{dan} x {n} = {dan * n}")
```

## 연습문제

1. 1부터 100까지 중 3의 배수의 합을 구하세요.
2. 구구단 7단을 출력하세요.
3. 사용자가 `q`를 입력할 때까지 숫자를 계속 입력받아, 마지막에 합계를 출력하세요.

??? success "해답"
    ```python
    # 1
    print(sum(n for n in range(1, 101) if n % 3 == 0))   # 1683

    # 2
    for n in range(1, 10):
        print(f"7 x {n} = {7 * n}")

    # 3
    total = 0
    while True:
        text = input("숫자 (끝내려면 q): ")
        if text == "q":
            break
        total += int(text)
    print("합계:", total)
    ```
