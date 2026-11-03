# 08. 파일 입출력

## open과 with

```python
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write("안녕\n")
```

- `with` 블록이 끝나면 파일이 **자동으로 닫힙니다.** 직접 `f.close()`를 부를 필요가 없습니다.
- 두 번째 인자는 **모드**입니다.

| 모드 | 뜻 |
|---|---|
| `"r"` | 읽기 (기본값). 파일이 없으면 오류 |
| `"w"` | 쓰기. **기존 내용을 지우고** 새로 씀 |
| `"a"` | 이어 쓰기. 끝에 덧붙임 |
| `"x"` | 새로 만들기. 이미 있으면 오류 (덮어쓰기 방지) |
| `"b"` 추가 | 바이너리 (`"rb"`, `"wb"`) — 이미지 등 |

!!! warning "Windows에서는 encoding을 꼭 적으세요"
    `encoding`을 생략하면 Windows에서는 운영체제 기본값(한국어 Windows는 보통 CP949)으로 읽고 씁니다. 그래서 다른 PC나 GitHub Actions(리눅스)에서 한글이 깨지거나 `UnicodeDecodeError`가 날 수 있습니다. **항상 `encoding="utf-8"`**을 적는 습관을 들이세요.

## 실행해 보기

```python title="examples/ch08_files.py"
--8<-- "examples/ch08_files.py"
```

이 예제는 `Path(__file__).resolve().parent`(이 파일이 있는 폴더)를 기준으로 경로를 만들기 때문에, 어느 폴더에서 실행해도 `examples\_out\memo.txt`에 저장됩니다. [01장](01-setup.md#하위-폴더에서-실행하면-파일을-못-찾는-이유)에서 본 "현재 폴더" 문제를 피하는 방법입니다.

## 읽는 여러 방법

```python
with open(path, encoding="utf-8") as f:
    whole = f.read()          # 전체를 문자열 하나로

with open(path, encoding="utf-8") as f:
    lines = f.readlines()     # 줄 단위 리스트 (끝에 \n 포함)

with open(path, encoding="utf-8") as f:
    for line in f:            # 한 줄씩 (큰 파일에 적합)
        print(line.rstrip("\n"))
```

## CSV 파일

쉼표로 구분된 표 데이터는 표준 라이브러리 `csv`로 다룹니다. 엑셀에서 연 CSV의 한글이 깨지면 `encoding="utf-8-sig"`로 저장해 보세요.

```python
import csv

with open("scores.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["이름", "점수"])
    writer.writerow(["민수", 80])

with open("scores.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        print(row["이름"], int(row["점수"]))
```

## 연습문제

1. 1부터 5까지 숫자를 한 줄에 하나씩 `numbers.txt`에 쓰고, 다시 읽어 합계를 출력하세요.
2. 기존 파일을 덮어쓰지 않도록 `"x"` 모드로 파일을 만들고, 이미 있을 때 나는 오류 이름을 확인하세요.

??? success "해답"
    ```python
    from pathlib import Path
    import tempfile

    folder = Path(tempfile.mkdtemp())     # 연습용 임시 폴더
    path = folder / "numbers.txt"

    # 1
    with open(path, "w", encoding="utf-8") as f:
        for n in range(1, 6):
            f.write(f"{n}\n")
    with open(path, encoding="utf-8") as f:
        print(sum(int(line) for line in f))   # 15

    # 2
    try:
        with open(path, "x", encoding="utf-8") as f:
            f.write("새 파일")
    except FileExistsError as e:
        print("이미 있음:", type(e).__name__)  # FileExistsError
    ```
