# 부록: 자주 만나는 오류

오류 메시지는 **맨 아래 줄부터** 읽으세요. 아래 표에서 비슷한 메시지를 찾아보세요.

## 실행·설치

| 메시지 | 흔한 원인 | 해결 |
|---|---|---|
| `'python' 용어가 cmdlet, 함수... 이름으로 인식되지 않습니다` | 파이썬이 PATH에 없음 | 설치 시 **Add to PATH** 체크, PowerShell 새로 열기, 또는 `py` 사용 |
| `can't open file '...\x.py': [Errno 2] No such file or directory` | 현재 폴더에 그 파일이 없음 | `pwd`, `ls`로 확인 후 `cd` ([01장](01-setup.md)) |
| `ModuleNotFoundError: No module named 'requests'` | 패키지 미설치, 또는 다른 파이썬/가상환경 | 가상환경 활성화 확인 후 `python -m pip install requests` |
| `ModuleNotFoundError: No module named 'myapp'` | `-m` 실행 위치가 패키지 부모 폴더가 아님 | `ls`에 `myapp` 폴더가 보이는 곳에서 실행 ([사례 학습](18-case-python-m.md)) |
| `ImportError: attempted relative import with no known parent package` | 상대 import가 있는 파일을 경로로 직접 실행 | `python -m 패키지.모듈`로 실행 |
| `이 시스템에서 스크립트를 실행할 수 없으므로 ...Activate.ps1` | PowerShell 실행 정책 | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` ([10장](10-modules.md)) |
| `OSError: [WinError 10048]` / `Address already in use` | 같은 포트를 이미 사용 중 | 기존 서버 종료 또는 다른 `--port` |

## 문법

| 메시지 | 흔한 원인 |
|---|---|
| `SyntaxError: invalid syntax` | 콜론(`:`) 누락, 괄호·따옴표 짝 안 맞음 |
| `SyntaxError: expected ':'` | `if`, `for`, `def` 줄 끝의 `:` 누락 |
| `IndentationError: expected an indented block` | `:` 다음 줄을 들여 쓰지 않음 |
| `IndentationError: unindent does not match` | 탭과 공백을 섞어 씀 → 공백 4칸으로 통일 |

## 실행 중

| 메시지 | 흔한 원인 |
|---|---|
| `NameError: name 'x' is not defined` | 오타, 정의 전에 사용, 다른 함수의 지역 변수 |
| `TypeError: can only concatenate str (not "int") to str` | `"나이: " + 30` → `f"나이: {30}"` 또는 `str(30)` |
| `TypeError: 'NoneType' object is not subscriptable` | `return` 없는 함수의 결과(None)를 `x[0]`처럼 사용 |
| `AttributeError: 'list' object has no attribute 'add'` | 그 자료형에 없는 메서드 (리스트는 `append`) |
| `KeyError: 'email'` | 딕셔너리에 없는 키 → `get("email")` |
| `IndexError: list index out of range` | 리스트 길이보다 큰 번호 |
| `ValueError: invalid literal for int() with base 10: 'abc'` | 숫자가 아닌 문자열을 `int()` |
| `UnicodeDecodeError: 'cp949' codec can't decode` | `encoding="utf-8"` 없이 UTF-8 파일을 읽음 |
| `json.decoder.JSONDecodeError` | JSON 형식이 아님 (빈 문자열, 작은따옴표, 끝에 쉼표 등) |
| `requests.exceptions.ConnectTimeout` / `ReadTimeout` | 네트워크 문제 또는 서버 무응답 |
| `smtplib.SMTPAuthenticationError` | 메일 계정·앱 비밀번호 오류, SMTP 사용 설정 안 됨 |

## 그래도 모르겠다면

1. 오류 메시지 **마지막 줄**을 그대로 검색해 보세요.
2. 문제를 재현하는 **가장 짧은 코드**를 만들어 보세요. 줄이다 보면 원인이 보이는 경우가 많습니다.
3. 질문할 때는 실행한 명령, 현재 폴더(`pwd`), 파이썬 버전(`python --version`), 전체 오류 메시지를 함께 적으세요. 단, **비밀번호·API 키·개인정보는 지우고** 올리세요.
