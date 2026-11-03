# 10. 모듈·패키지·pip·venv

프로그램이 커지면 코드를 여러 파일로 나눕니다. 이 장에서는 파일을 나누고 불러오는 방법(`import`)과, 남이 만든 라이브러리를 설치하고 관리하는 방법(`pip`, 가상환경, `requirements.txt`)을 배웁니다.

## 모듈과 패키지

- **모듈**: `.py` 파일 하나. `ops.py`는 `ops` 모듈입니다.
- **패키지**: 모듈을 모아 둔 **폴더**. 폴더 안에 `__init__.py`를 두면 확실하게 패키지로 취급됩니다.

```text
ch10_modules/          ← 여기서 python main.py 를 실행
├── main.py
└── calc/              ← calc 패키지
    ├── __init__.py    ← import calc 할 때 실행되는 파일
    └── ops.py         ← calc.ops 모듈
```

```python title="examples/ch10_modules/calc/__init__.py"
--8<-- "examples/ch10_modules/calc/__init__.py"
```

```python title="examples/ch10_modules/calc/ops.py"
--8<-- "examples/ch10_modules/calc/ops.py"
```

```python title="examples/ch10_modules/main.py"
--8<-- "examples/ch10_modules/main.py"
```

```powershell
cd examples\ch10_modules
python main.py
python -m calc.ops      # 패키지 안의 모듈을 '모듈 이름'으로 실행
```

## import의 여러 형태

| 형태 | 사용할 때 |
|---|---|
| `import math` | `math.sqrt(4)`처럼 모듈 이름을 붙여 사용 |
| `from math import sqrt` | `sqrt(4)`처럼 바로 사용 |
| `import calc.ops as ops` | 긴 이름에 별명 붙이기 |
| `from .ops import add` | **상대 import**: 같은 패키지 안의 모듈 ([사례 학습](18-case-python-m.md)) |

## 파이썬은 모듈을 어디서 찾나 — sys.path

`import calc`라고 쓰면 파이썬은 `sys.path`에 적힌 폴더들을 **순서대로** 뒤져 `calc.py`나 `calc` 폴더를 찾습니다. 첫 번째 칸에는 다음이 들어갑니다.

- `python main.py`로 실행하면 → **main.py가 있는 폴더**
- `python -m 모듈`로 실행하면 → **현재 폴더**

그래서 엉뚱한 폴더에서 실행하면 `ModuleNotFoundError: No module named 'calc'`가 납니다. 확인하려면:

```python
import sys
print(sys.path)
```

!!! danger "표준 라이브러리와 같은 이름의 파일을 만들지 마세요"
    내 폴더에 `json.py`, `random.py`, `email.py` 같은 파일을 만들면 표준 라이브러리 대신 **내 파일이 먼저 import**되어 이상한 오류가 납니다.

## pip: 외부 패키지 설치

파이썬 패키지 저장소 [PyPI](https://pypi.org/)의 라이브러리는 `pip`로 설치합니다.

```powershell
python -m pip install requests        # 설치
python -m pip install "requests==2.32.3"  # 버전 지정
python -m pip list                    # 설치된 목록
python -m pip show requests           # 정보 (버전, 라이선스 등)
python -m pip uninstall requests      # 삭제
```

!!! tip "`pip` 대신 `python -m pip`"
    `python -m pip`라고 쓰면 **지금 쓰는 그 파이썬**에 설치된다는 것이 확실합니다. PC에 파이썬이 여러 개 있을 때 엉뚱한 곳에 설치되는 일을 막아 줍니다.

!!! warning "외부 패키지를 설치하기 전에"
    - 이름이 비슷한 가짜 패키지(타이포스쿼팅)가 있습니다. 철자와 PyPI 페이지의 공식 저장소 링크, 내려받기 수, 관리 상태를 확인하세요.
    - 회사나 팀 프로젝트라면 **라이선스**(MIT, BSD, Apache-2.0, GPL 등)를 확인하고, 사용 가능 여부는 담당 부서에 문의하세요. `python -m pip show 패키지`의 `License` 항목에서 단서를 볼 수 있습니다.

## 가상환경(venv)

프로젝트마다 필요한 패키지와 버전이 다릅니다. **가상환경**은 프로젝트 폴더 안에 "그 프로젝트 전용 파이썬 + 패키지 공간"을 만들어 서로 섞이지 않게 합니다.

```powershell
cd D:\study\myapp
python -m venv .venv               # .venv 폴더에 가상환경 생성 (한 번만)
.\.venv\Scripts\Activate.ps1       # 활성화 → 프롬프트 앞에 (.venv) 표시
python -m pip install requests     # 이제 .venv 안에만 설치됨
deactivate                         # 비활성화
```

!!! warning "Activate.ps1 실행이 막힐 때"
    `이 시스템에서 스크립트를 실행할 수 없으므로...`라는 오류가 나면, 현재 PowerShell 창에서만 허용하는 방법이 있습니다.
    ```powershell
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
    또는 활성화 없이 가상환경의 파이썬을 직접 부를 수도 있습니다: `.\.venv\Scripts\python.exe main.py`
    회사 PC라면 보안 정책을 바꾸기 전에 IT 담당자에게 확인하세요.

`.venv` 폴더는 git에 올리지 않습니다. `.gitignore`에 `.venv/`를 적어 두세요. ([17장](17-git-github.md))

## requirements.txt

"이 프로젝트에 필요한 패키지 목록"을 파일로 남겨 두면, 다른 PC나 GitHub Actions에서도 같은 환경을 만들 수 있습니다.

```text title="requirements.txt"
requests==2.32.3
Jinja2==3.1.6
```

```powershell
python -m pip install -r requirements.txt     # 목록대로 설치
python -m pip freeze > requirements.txt       # 현재 설치된 목록을 파일로 (모든 하위 의존성까지 포함)
```

`==`로 버전을 고정하면 "어제는 됐는데 오늘은 안 되는" 일을 줄일 수 있습니다.

## 연습문제

1. `ch10_modules\calc` 패키지에 `subtract(a, b)`를 추가하고 `main.py`에서 `from calc import subtract`로 쓸 수 있게 하세요.
2. `ch10_modules\calc` 폴더 **안에서** `python ..\main.py`를 실행하면 될까요? `python -m main`은요? 이유를 설명해 보세요.
3. 새 폴더에 가상환경을 만들고 `requests`를 설치한 뒤, `requirements.txt`를 만드세요.

??? success "해답"
    1. `ops.py`에 함수를 추가하고, `__init__.py`의 import 줄을 `from .ops import add, multiply, subtract`로 바꿉니다.
    2. `python ..\main.py`는 **동작합니다.** 파일 경로로 실행하면 `sys.path` 첫 칸이 main.py가 있는 폴더(ch10_modules)가 되므로 `calc`를 찾습니다.
       `python -m main`은 **실패합니다.** `-m`은 현재 폴더(calc)를 기준으로 `main` 모듈을 찾는데, 거기에는 main.py가 없기 때문입니다(`No module named main`).
    3. ```powershell
       mkdir D:\study\venv-test; cd D:\study\venv-test
       python -m venv .venv
       .\.venv\Scripts\Activate.ps1
       python -m pip install requests
       python -m pip freeze > requirements.txt
       ```
