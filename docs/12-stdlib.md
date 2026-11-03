# 12. 표준 라이브러리

파이썬은 설치만 하면 바로 쓸 수 있는 **표준 라이브러리**가 매우 풍부합니다. `pip`로 설치할 필요가 없습니다. 실무에서 특히 자주 쓰는 다섯 가지를 봅니다.

## json

JSON은 웹과 설정 파일에서 가장 많이 쓰는 데이터 형식입니다. 파이썬의 딕셔너리·리스트와 거의 1:1로 대응합니다.

| JSON | 파이썬 |
|---|---|
| `{"a": 1}` 객체 | `dict` |
| `[1, 2]` 배열 | `list` |
| `"text"` | `str` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

| 함수 | 방향 |
|---|---|
| `json.dumps(obj)` | 파이썬 객체 → JSON **문자열** |
| `json.loads(text)` | JSON 문자열 → 파이썬 객체 |
| `json.dump(obj, f)` / `json.load(f)` | 파일에 직접 쓰기 / 읽기 |

한글을 `\uXXXX`로 바꾸지 않고 그대로 저장하려면 `ensure_ascii=False`, 보기 좋게 줄을 맞추려면 `indent=2`를 줍니다.

## pathlib

`pathlib.Path`는 파일 경로를 문자열이 아닌 **객체**로 다룹니다. `/` 연산자로 경로를 이을 수 있고, Windows의 `\`와 리눅스의 `/` 차이를 알아서 처리합니다.

```python
from pathlib import Path

here = Path(__file__).resolve().parent   # 이 .py 파일이 있는 폴더 (어디서 실행해도 같음)
root = here.parent                       # 그 부모 폴더
config = root / "config" / "app.json"    # 경로 잇기

config.exists(), config.is_file()        # 있는지, 파일인지
config.name, config.stem, config.suffix  # 'app.json', 'app', '.json'
config.read_text(encoding="utf-8")       # 파일 전체 읽기
(root / "out").mkdir(parents=True, exist_ok=True)   # 폴더 만들기 (이미 있어도 OK)
list(root.glob("*.py"))                  # 패턴으로 파일 찾기
Path.cwd()                               # 현재 폴더
```

!!! tip "Path(__file__) 와 Path.cwd() 의 차이"
    `Path.cwd()`는 **실행한 위치**에 따라 바뀌고, `Path(__file__).resolve().parent`는 **파일 위치**라서 바뀌지 않습니다. 프로그램에 딸린 설정·템플릿 파일을 찾을 때는 후자를 쓰세요. ([01장](01-setup.md))

```python title="examples/ch12_json_pathlib.py"
--8<-- "examples/ch12_json_pathlib.py"
```

## datetime

```python title="examples/ch12_datetime.py"
--8<-- "examples/ch12_datetime.py"
```

| 서식 코드 | 뜻 | 예 |
|---|---|---|
| `%Y` `%m` `%d` | 연·월·일 | 2026 11 03 |
| `%H` `%M` `%S` | 시·분·초 (24시간) | 07 30 00 |
| `%a` | 요일 약자 | Tue |

!!! note "시간대(time zone)를 신경 쓰세요"
    `datetime.now()`는 **그 컴퓨터의 시간대**를 따릅니다. 내 PC는 한국 시간이어도 GitHub Actions 서버는 보통 **UTC**(한국보다 9시간 느림)입니다. 서버에서 "오늘 날짜"를 구할 때는 위 예제처럼 시간대를 명시하세요. `zoneinfo.ZoneInfo("Asia/Seoul")`도 쓸 수 있지만, Windows에서는 `pip install tzdata`가 필요할 수 있습니다.

## argparse

명령줄에서 옵션을 받는 프로그램을 만듭니다. `--help`를 자동으로 만들어 줍니다.

```python title="examples/ch12_argparse.py"
--8<-- "examples/ch12_argparse.py"
```

```powershell
python ch12_argparse.py --help
python ch12_argparse.py 민수 --times 2 --shout
```

| 옵션 정의 | 의미 |
|---|---|
| `add_argument("name")` | 필수 위치 인자 |
| `add_argument("--times", type=int, default=1)` | 선택 옵션, 정수로 변환 |
| `add_argument("--shout", action="store_true")` | 붙이면 `True`, 안 붙이면 `False` |

## subprocess

파이썬에서 다른 프로그램(git, 다른 파이썬 스크립트 등)을 실행합니다.

```python title="examples/ch12_subprocess.py"
--8<-- "examples/ch12_subprocess.py"
```

!!! danger "shell=True 와 사용자 입력"
    `subprocess.run(f"git log {user_input}", shell=True)`처럼 **사용자 입력을 명령 문자열에 끼워 넣으면** 입력에 `; del ...` 같은 명령을 섞어 실행시킬 수 있습니다(명령 주입). 위 예제처럼 **리스트로 인자를 나눠 전달**하고 `shell=True`는 피하세요.

## 연습문제

1. `{"date": "2026-11-03", "items": ["a", "b"]}`를 `data.json`으로 저장한 뒤 다시 읽어 `items`의 개수를 출력하세요.
2. 오늘부터 크리스마스(12월 25일)까지 며칠 남았는지 출력하세요.
3. 파일 경로를 인자로 받아 그 파일의 줄 수를 출력하는 `count_lines.py`를 argparse로 만드세요.

??? success "해답"
    ```python
    import json
    import tempfile
    from datetime import date
    from pathlib import Path

    # 1
    path = Path(tempfile.mkdtemp()) / "data.json"
    path.write_text(json.dumps({"date": "2026-11-03", "items": ["a", "b"]}), encoding="utf-8")
    print(len(json.loads(path.read_text(encoding="utf-8"))["items"]))   # 2

    # 2
    today = date.today()
    xmas = date(today.year, 12, 25)
    if xmas < today:
        xmas = date(today.year + 1, 12, 25)
    print((xmas - today).days, "일 남음")
    ```

    ```python title="count_lines.py (3번)"
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="줄 수 세기")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    print(len(args.path.read_text(encoding="utf-8").splitlines()))
    ```
