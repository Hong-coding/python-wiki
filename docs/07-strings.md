# 07. 문자열

문자열(`str`)은 글자들이 순서대로 늘어선 값입니다. 작은따옴표와 큰따옴표 모두 쓸 수 있고, 여러 줄은 `"""`로 감쌉니다.

## 자주 쓰는 메서드

| 메서드 | 예 → 결과 |
|---|---|
| `strip()` | `"  hi  ".strip()` → `'hi'` (앞뒤 공백 제거) |
| `lower()` / `upper()` | `"Hi".lower()` → `'hi'` |
| `replace(a, b)` | `"a-b".replace("-", "+")` → `'a+b'` |
| `split(sep)` | `"a,b,c".split(",")` → `['a', 'b', 'c']` |
| `sep.join(list)` | `"-".join(["a", "b"])` → `'a-b'` |
| `startswith` / `endswith` | `"report.csv".endswith(".csv")` → `True` |
| `find(x)` | `"hello".find("l")` → `2` (없으면 `-1`) |
| `isdigit()` | `"123".isdigit()` → `True` |

!!! note "문자열은 바꿀 수 없습니다(immutable)"
    `s.upper()`는 `s`를 바꾸지 않고 **새 문자열을 돌려줍니다.** 결과를 쓰려면 `s = s.upper()`처럼 다시 대입하세요.

## 실행해 보기

```python title="examples/ch07_strings.py"
--8<-- "examples/ch07_strings.py"
```

## f-string 서식

| 서식 | 예 | 결과 |
|---|---|---|
| 소수점 | `f"{3.14159:.2f}"` | `3.14` |
| 천 단위 쉼표 | `f"{1234567:,}"` | `1,234,567` |
| 폭·정렬 | `f"{'a':>5}"` | `'    a'` |
| 0 채우기 | `f"{7:03d}"` | `007` |
| 디버깅 | `f"{x=}"` | `x=10` |

## 이스케이프 문자와 raw 문자열

`\n`은 줄바꿈, `\t`는 탭입니다. Windows 경로처럼 `\`가 많을 때는 앞에 `r`을 붙인 **raw 문자열**을 쓰면 `\`가 그대로 유지됩니다.

```python
print("C:\new")    # \n 이 줄바꿈으로 바뀌어 버림
print(r"C:\new")   # C:\new
```

## 인코딩: 문자열과 바이트

화면의 글자(`str`)와 파일·네트워크로 오가는 바이트(`bytes`)는 다릅니다. 둘 사이를 바꾸는 규칙이 인코딩이며, 요즘은 **UTF-8**을 씁니다.

```python
data = "한글".encode("utf-8")   # b'\xed\x95\x9c\xea\xb8\x80'
text = data.decode("utf-8")     # '한글'
```

## 연습문제

1. `"  Python is FUN  "`을 앞뒤 공백 없이 모두 소문자로 바꾸세요.
2. `"2026-11-03"`을 `split`해서 `"2026년 11월 3일"`로 출력하세요.
3. 문장 `"나는 파이썬을 좋아한다 파이썬은 재밌다"`에서 `"파이썬"`이 몇 번 나오는지 세세요.

??? success "해답"
    ```python
    print("  Python is FUN  ".strip().lower())       # python is fun

    year, month, day = "2026-11-03".split("-")
    print(f"{year}년 {int(month)}월 {int(day)}일")    # 2026년 11월 3일

    print("나는 파이썬을 좋아한다 파이썬은 재밌다".count("파이썬"))   # 2
    ```
