# 15. 메일 보내기와 시크릿 관리

## 시크릿이란?

비밀번호, API 키, 토큰처럼 **남이 알면 안 되는 값**을 시크릿이라고 합니다. 가장 중요한 원칙은 하나입니다.

!!! danger "시크릿을 코드에 직접 쓰지 마세요"
    ```python
    password = "abcd1234"   # ❌ 절대 이렇게 쓰지 않습니다
    ```
    코드는 git에 올라가고, 한 번 올라간 값은 커밋 기록에 계속 남습니다. 공개 저장소라면 몇 분 안에 자동 수집기가 가져갈 수 있습니다. 실수로 올렸다면 **즉시 그 비밀번호·키를 폐기하고 새로 발급**하세요. 파일만 지우는 것으로는 부족합니다.

대신 **환경변수**로 받습니다.

## 환경변수

환경변수는 프로그램 바깥(운영체제)에서 프로그램에 넘겨주는 `이름=값` 설정입니다.

```powershell
$env:APP_MODE = "dev"          # 현재 PowerShell 창에서만 유효
python -c "import os; print(os.environ.get('APP_MODE'))"
Remove-Item Env:APP_MODE       # 삭제
```

```python
import os

os.environ["SMTP_USER"]               # 없으면 KeyError
os.environ.get("SMTP_PORT", "587")    # 없으면 기본값
```

## .env 파일

매번 `$env:...`를 입력하기 번거로우므로, 로컬 개발 때는 프로젝트 최상위 폴더에 `.env` 파일을 두고 읽어 들이는 방식을 많이 씁니다.

```text title=".env (예시 — git 에 올리지 않음)"
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=me@example.com
SMTP_PASSWORD=여기에-실제-값
MAIL_TO=you@example.com
```

- `.env`는 **반드시 `.gitignore`에 추가**합니다.
- 대신 값이 비어 있는 `.env.example`을 저장소에 올려 "어떤 설정이 필요한지" 알려 줍니다.
- 처음 설정할 때는 `.env.example`이 있는 폴더(보통 최상위)로 이동해서 복사합니다. 이미 `.env`가 있으면 덮어쓰지 않도록 주의하세요.

```powershell
cd D:\study\myapp              # .env.example 이 있는 폴더
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
notepad .env
```

### 실행해 보기: 간단한 .env 로더

```python title="examples/ch15_dotenv.py"
--8<-- "examples/ch15_dotenv.py"
```

실무에서는 [python-dotenv](https://pypi.org/project/python-dotenv/) 패키지를 많이 씁니다. 외부 패키지를 쓰기 전에는 신뢰성과 라이선스를 확인하세요. ([10장](10-modules.md#pip-외부-패키지-설치))

## smtplib로 메일 보내기

메일은 **SMTP** 서버를 통해 보냅니다. 파이썬 표준 라이브러리 `smtplib`(보내기)와 `email.message`(메일 만들기)를 씁니다.

```python title="examples/ch15_email.py"
--8<-- "examples/ch15_email.py"
```

```powershell
python ch15_email.py           # 미리보기만 (발송 안 함)
python ch15_email.py --send    # 환경변수를 설정한 뒤 실제 발송
```

| 단계 | 코드 | 설명 |
|---|---|---|
| 1 | `EmailMessage()` | 메일 객체 만들기 |
| 2 | `set_content` / `add_alternative` | 텍스트·HTML 본문 |
| 3 | `smtplib.SMTP(host, 587)` | 서버 연결 |
| 4 | `starttls()` | 암호화 시작 |
| 5 | `login(user, password)` | 로그인 |
| 6 | `send_message(msg)` | 발송 |

!!! note "Gmail 등 메일 서비스의 설정"
    많은 메일 서비스는 계정 비밀번호로 SMTP 로그인을 막아 두고, **앱 비밀번호**나 OAuth를 요구합니다. 사용하는 서비스의 공식 도움말에서 SMTP 서버 주소·포트·인증 방법을 확인하세요. 회사 메일 계정을 외부 프로그램에 연결할 때는 사내 보안 정책도 확인하세요.

!!! warning "메일 주소도 개인정보입니다"
    수신자 목록을 로그나 오류 메시지에 그대로 찍지 말고, 공개 저장소에 올리지 마세요. 예제처럼 `{len(to)}명` 정도만 출력하는 것이 안전합니다.

## GitHub Actions에서 시크릿 쓰기

GitHub 저장소의 **Settings → Secrets and variables → Actions**에 시크릿을 등록하면, 워크플로에서 환경변수로 넘길 수 있습니다. 로그에는 `***`로 가려져 표시됩니다. ([17장](17-git-github.md#github-actions-로-예약-실행))

```yaml
- run: python ch15_email.py --send
  env:
    SMTP_HOST: ${{ secrets.SMTP_HOST }}
    SMTP_USER: ${{ secrets.SMTP_USER }}
    SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
    MAIL_TO: ${{ secrets.MAIL_TO }}
```

## 연습문제

1. `APP_MODE` 환경변수가 `prod`이면 "운영 모드", 아니면 "개발 모드"를 출력하는 코드를 쓰세요.
2. `ch15_email.py`에서 `MAIL_TO`에 주소가 하나도 없으면 오류 메시지를 출력하고 종료 코드 2로 끝나게 바꾸세요.
3. API 키를 출력할 때 앞 4글자만 보이고 나머지는 `*`로 가리는 `mask(secret)` 함수를 만드세요.

??? success "해답"
    ```python
    import os

    # 1
    print("운영 모드" if os.environ.get("APP_MODE") == "prod" else "개발 모드")

    # 3
    def mask(secret: str) -> str:
        return secret[:4] + "*" * max(len(secret) - 4, 0)

    print(mask("sk-1234567890"))   # sk-1*********
    ```

    2번: `to`를 만든 직후에 추가합니다.
    ```python title="ch15_email.py 에 추가"
    if not to:
        print("[오류] MAIL_TO 가 비어 있습니다", file=sys.stderr)   # 파일 위쪽에 import sys
        sys.exit(2)
    ```
