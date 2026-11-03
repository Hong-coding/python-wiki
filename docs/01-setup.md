# 01. 설치와 실행 환경

이 장에서는 파이썬을 설치하고, PowerShell에서 파이썬 파일을 실행하는 방법을 배웁니다. 그리고 초보자가 가장 많이 막히는 **"현재 폴더"** 개념을 확실히 잡습니다.

## 파이썬 설치 (Windows)

1. <https://www.python.org/downloads/> 에서 최신 Python 3 설치 파일을 받습니다.
2. 설치 첫 화면에서 **Add python.exe to PATH**에 체크한 뒤 **Install Now**를 누릅니다.
3. 설치가 끝나면 PowerShell을 **새로** 엽니다. (열려 있던 창은 PATH 변경을 모릅니다.)

```powershell
python --version
```

`Python 3.13.x`처럼 버전이 나오면 성공입니다.

!!! warning "Microsoft Store 창이 뜨는 경우"
    `python`을 입력했는데 Microsoft Store가 열리면, 실제 파이썬 대신 Windows의 '바로가기'가 실행된 것입니다.
    **설정 → 앱 → 고급 앱 설정 → 앱 실행 별칭**에서 `python.exe`, `python3.exe` 항목을 끄고 PowerShell을 다시 여세요.
    또는 `py` 명령(파이썬 런처)을 써도 됩니다: `py --version`

## 대화형 모드(REPL)와 파일 실행

파이썬은 두 가지 방식으로 실행할 수 있습니다.

=== "대화형 모드"

    ```powershell
    python
    ```
    ```text
    >>> 1 + 2
    3
    >>> print("안녕")
    안녕
    >>> exit()
    ```
    한 줄씩 바로 결과를 볼 수 있어 실험할 때 좋습니다.

=== "파일 실행"

    `hello.py` 파일을 만들고 아래 내용을 저장합니다. (메모장보다는 [VS Code](https://code.visualstudio.com/)를 권장합니다.)
    ```python
    print("안녕하세요, 파이썬!")
    ```
    ```powershell
    python hello.py
    ```

!!! note "파일은 UTF-8로 저장하세요"
    한글이 깨지면 편집기에서 파일 인코딩을 **UTF-8**로 저장했는지 확인하세요. VS Code는 기본이 UTF-8입니다.

## 현재 폴더(작업 디렉터리)란?

PowerShell 창은 항상 **어떤 폴더 하나 "안에" 서 있습니다.** 이 폴더를 **현재 폴더**(current working directory, cwd)라고 합니다. 프롬프트 앞부분에 보입니다.

```text
PS C:\Users\me>          ← 지금 C:\Users\me 폴더 안에 있음
```

자주 쓰는 명령은 다음과 같습니다.

| 명령 | 뜻 | 예 |
|---|---|---|
| `pwd` | 현재 폴더 보기 | `pwd` |
| `ls` (`dir`) | 현재 폴더의 파일 목록 | `ls` |
| `cd 폴더` | 그 폴더로 이동 | `cd D:\study\python-wiki` |
| `cd ..` | 한 단계 위(부모) 폴더로 | `cd ..` |
| `cd ~` | 내 사용자 폴더로 | `cd ~` |

!!! tip "드라이브 이동과 공백 있는 경로"
    - `cd D:\study`처럼 드라이브를 포함해 쓰면 다른 드라이브로도 이동합니다.
    - 경로에 공백이 있으면 따옴표로 감쌉니다: `cd "C:\My Projects\wiki"`
    - 파일 탐색기 주소창에 `powershell`이라고 입력하고 Enter를 누르면, **그 폴더가 현재 폴더인** PowerShell이 열립니다.
    - `Tab` 키를 누르면 폴더·파일 이름이 자동 완성됩니다.

## 하위 폴더에서 실행하면 파일을 못 찾는 이유

다음과 같은 프로젝트가 있다고 합시다.

```text
D:\study\myapp\            ← 프로젝트 최상위 폴더
├── .env.example
├── data.txt
└── myapp\
    └── main.py
```

`main.py`에 `open("data.txt")`라고 썼다면, 파이썬은 `data.txt`를 **main.py가 있는 곳이 아니라 "현재 폴더"에서** 찾습니다.

```powershell
cd D:\study\myapp          # 최상위 폴더에서 실행 → data.txt 를 찾음 ✅
python myapp\main.py

cd D:\study\myapp\myapp    # 하위 폴더에서 실행 → 여기엔 data.txt 가 없음 ❌
python main.py             # FileNotFoundError: [Errno 2] No such file or directory: 'data.txt'
```

PowerShell 명령도 마찬가지입니다. 하위 폴더에 들어가 있으면 `Copy-Item .env.example .env`는 하위 폴더에서 `.env.example`을 찾으므로 실패합니다. **"이 파일이 어느 폴더에 있는지"와 "내가 지금 어느 폴더에 서 있는지"를 항상 함께 확인하세요.**

```powershell
pwd                        # 1) 지금 어디인지 확인
ls                         # 2) 찾는 파일이 보이는지 확인
cd D:\study\myapp          # 3) 안 보이면 그 파일이 있는 폴더로 이동
```

### 실행해 보기

```python title="examples/ch01_where_am_i.py"
--8<-- "examples/ch01_where_am_i.py"
```

`examples` 폴더와 그 부모 폴더에서 각각 실행해 보고, 첫 줄(현재 폴더)이 어떻게 달라지는지 비교하세요.

```powershell
cd python-wiki\examples
python ch01_where_am_i.py
cd ..
python examples\ch01_where_am_i.py
```

!!! success "해결책: 파일 위치 기준 경로"
    `Path(__file__).resolve().parent`는 "이 .py 파일이 있는 폴더"입니다. 이것을 기준으로 경로를 만들면 **어디서 실행해도** 같은 파일을 찾습니다. [12장 pathlib](12-stdlib.md#pathlib)에서 자세히 다룹니다.

## 연습문제

1. PowerShell에서 내 사용자 폴더로 이동한 뒤, 현재 폴더를 출력해 보세요.
2. `D:\study\myapp\myapp` 안에 있을 때, 최상위 폴더의 `.env.example`을 `.env`로 복사하려면 어떻게 해야 할까요? (두 가지 방법)
3. `python hello.py`를 실행했더니 `can't open file '...hello.py': [Errno 2] No such file or directory`가 나왔습니다. 무엇을 확인해야 할까요?

??? success "해답"
    1. `cd ~` 다음 `pwd`.
    2. ① 최상위로 이동해서 복사: `cd ..` 후 `Copy-Item .env.example .env`
       ② 이동하지 않고 상대 경로로 지정: `Copy-Item ..\.env.example ..\.env`
       이미 `.env`가 있다면 덮어쓰지 않도록 먼저 `Test-Path ..\.env`로 확인하세요.
    3. `pwd`로 현재 폴더를 보고, `ls`로 그 폴더에 `hello.py`가 실제로 있는지 확인합니다. 없다면 `cd`로 파일이 있는 폴더로 이동하거나, `python D:\경로\hello.py`처럼 전체 경로를 씁니다.
