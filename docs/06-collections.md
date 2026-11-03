# 06. 리스트와 딕셔너리

여러 값을 한데 묶어 다루는 자료형을 배웁니다.

| 자료형 | 모양 | 특징 |
|---|---|---|
| 리스트 `list` | `[1, 2, 3]` | 순서 있음, 수정 가능, 중복 가능 |
| 튜플 `tuple` | `(1, 2, 3)` | 순서 있음, **수정 불가** |
| 딕셔너리 `dict` | `{"a": 1}` | **키 → 값** 짝, 키로 찾기 |
| 집합 `set` | `{1, 2, 3}` | 순서 없음, **중복 없음** |

## 리스트

```python
nums = [10, 20, 30]
nums[0]        # 10  (번호는 0부터)
nums[-1]       # 30  (음수는 뒤에서부터)
nums[0:2]      # [10, 20]  (슬라이싱: 끝 번호는 포함하지 않음)
nums.append(40)     # 끝에 추가
nums.insert(0, 5)   # 0번 위치에 추가
nums.remove(20)     # 값 20을 삭제
last = nums.pop()   # 마지막 값을 꺼내며 삭제
len(nums)           # 개수
```

## 딕셔너리

```python
person = {"name": "민수", "age": 30}
person["name"]              # '민수'
person["email"]             # KeyError! — 없는 키
person.get("email")         # None (오류 없이)
person.get("email", "-")    # '-' (기본값 지정)
person["age"] = 31          # 수정 / 추가
"name" in person            # True (키가 있는지)
del person["age"]           # 삭제
```

## 실행해 보기

```python title="examples/ch06_collections.py"
--8<-- "examples/ch06_collections.py"
```

## 리스트 컴프리헨션

"리스트를 만드는 반복문"을 한 줄로 쓰는 방법입니다.

```python
# 아래 두 코드는 같은 결과
squares = []
for n in range(5):
    squares.append(n * n)

squares = [n * n for n in range(5)]
```

딕셔너리도 같은 방법으로 만들 수 있습니다: `{w: len(w) for w in ["a", "bb"]}` → `{'a': 1, 'bb': 2}`

!!! note "JSON과 닮았습니다"
    딕셔너리와 리스트를 겹쳐 쓴 모양은 웹에서 데이터를 주고받는 **JSON** 형식과 거의 같습니다. [12장](12-stdlib.md)과 [사례 학습](18-case-python-m.md)에서 이 점을 활용합니다.

## 연습문제

1. `[3, 8, 1, 9, 4]`에서 가장 큰 값, 가장 작은 값, 합계를 출력하세요.
2. `["apple", "kiwi", "banana"]`를 글자 수가 긴 순서로 정렬하세요.
3. 학생 점수 딕셔너리 `{"민수": 80, "지은": 95, "철수": 70}`에서 평균 점수와 1등 이름을 구하세요.

??? success "해답"
    ```python
    nums = [3, 8, 1, 9, 4]
    print(max(nums), min(nums), sum(nums))           # 9 1 25

    fruits = ["apple", "kiwi", "banana"]
    print(sorted(fruits, key=len, reverse=True))     # ['banana', 'apple', 'kiwi']

    scores = {"민수": 80, "지은": 95, "철수": 70}
    print(sum(scores.values()) / len(scores))        # 81.66666666666667
    print(max(scores, key=scores.get))               # 지은
    ```
