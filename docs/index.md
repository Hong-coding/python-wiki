# 파이썬 A to Z

프로그래밍을 처음 배우는 분을 위한 한국어 파이썬 학습 위키입니다.
설치부터 시작해 변수·조건문·반복문 같은 기초를 익히고, 마지막에는 **웹에서 정보를 모아 메일로 보내고, 작은 관리 화면을 띄우고, GitHub Actions로 매일 자동 실행하는 프로그램**을 이해할 수 있도록 구성했습니다.

## 이 위키의 사용법

- 각 장은 **설명 → 실행해 볼 예제 → 연습문제** 순서로 되어 있습니다.
- 예제 코드 오른쪽 위의 :material-content-copy: 버튼을 누르면 코드가 복사됩니다.
- 연습문제의 해답은 접혀 있습니다. 먼저 직접 풀어 본 다음 펼쳐 보세요.
- 오른쪽 위 :material-weather-night: 버튼으로 다크 모드를 켜고 끌 수 있고, 검색창에서 용어를 찾을 수 있습니다.

## 예제 코드 받기

이 위키에 나오는 예제는 모두 저장소의 `examples` 폴더에 있습니다. 실제로 실행해서 확인한 코드이며, `tests/test_examples.py`가 매번 자동으로 다시 실행해 확인합니다.

```powershell
git clone https://github.com/Hong-coding/python-wiki.git
cd python-wiki\examples
python ch02_variables.py
```

git을 아직 모르면 GitHub 저장소 화면의 **Code → Download ZIP**으로 받아도 됩니다.

## 학습 순서

| 부 | 장 | 배우는 것 |
|---|---|---|
| 1부 기초 | [01](01-setup.md) ~ [05](05-functions.md) | 설치, 현재 폴더, 변수, 조건문, 반복문, 함수 |
| 2부 데이터 | [06](06-collections.md) ~ [09](09-exceptions.md) | 리스트·딕셔너리, 문자열, 파일, 예외 |
| 3부 구조 | [10](10-modules.md) ~ [12](12-stdlib.md) | 모듈·패키지·pip·venv, 클래스, 표준 라이브러리 |
| 4부 실전 | [13](13-web.md) ~ [17](17-git-github.md) | requests·RSS, 웹 서버·템플릿, 메일·시크릿, 테스트, git·Actions |
| 사례 | [18](18-case-python-m.md) | `python -m 패키지.모듈`은 어떻게 동작하나 |

!!! tip "처음이라면"
    [01. 설치와 실행 환경](01-setup.md)은 꼭 읽어 주세요. "파일을 못 찾는다"는 오류의 대부분은 **현재 폴더**를 몰라서 생깁니다.

## 대상 버전

- Python **3.11 이상**을 기준으로 씁니다. (예제는 3.12·3.13에서 실행해 확인했습니다.)
- 명령 예시는 **Windows PowerShell** 기준입니다. macOS·Linux에서는 `python` 대신 `python3`, 경로 구분자 `\` 대신 `/`를 쓰는 경우가 많습니다.
