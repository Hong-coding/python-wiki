# 파이썬 A to Z (python-wiki)

왕초보를 위한 한국어 파이썬 학습 위키입니다. 설치와 "현재 폴더" 개념부터 시작해 변수·조건문·함수, 파일·예외, 모듈·가상환경, 클래스, 표준 라이브러리, requests·RSS, `http.server`·Jinja2, 메일·시크릿 관리, 테스트, git·GitHub Actions까지 다룹니다. 마지막 사례 학습 장에서는 `python -m 패키지.모듈` 명령이 어떻게 동작하는지 따라가 봅니다.

- 위키 주소: https://hong-coding.github.io/python-wiki/
- 각 장 구성: 설명 → 실행해 볼 예제 → 연습문제와 해답(접기)

## 로컬에서 위키 띄우기 (Windows PowerShell)

```powershell
git clone https://github.com/Hong-coding/python-wiki.git
cd python-wiki
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
mkdocs serve
```

브라우저에서 http://127.0.0.1:8000/ 을 엽니다. 문서를 고치고 저장하면 화면이 자동으로 새로 고쳐집니다. 종료는 `Ctrl+C`입니다.

`Activate.ps1` 실행이 막히면 `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`를 먼저 실행하거나, 활성화하지 않고 `.\.venv\Scripts\mkdocs.exe serve`로 실행할 수 있습니다.

## 검증

```powershell
python -m unittest discover -s tests -v   # 예제 코드와 해답 코드 실행 테스트
mkdocs build --strict                      # 경고가 하나라도 있으면 실패
```

- `tests/test_examples.py`: `examples/`의 예제를 실제로 실행하고 출력을 확인합니다. 네트워크 예제는 테스트 안에서 띄운 로컬 서버(127.0.0.1)를 대상으로 실행합니다.
- `tests/test_doc_answers.py`: 문서의 연습문제 해답 코드 블록을 꺼내 실행합니다.
- GitHub Actions(`.github/workflows/deploy.yml`)가 `main`에 push될 때마다 위 두 단계를 실행하고, 통과하면 GitHub Pages에 배포합니다.

## 폴더 구조

```text
python-wiki/
├── mkdocs.yml            # 사이트 설정 (메뉴, 테마, 확장 기능)
├── requirements.txt      # 빌드·예제 실행에 필요한 패키지 (버전 고정)
├── docs/                 # 위키 본문 (Markdown)
├── examples/             # 본문에 포함되는 예제 코드 (문서에 그대로 삽입됨)
├── tests/                # 예제·해답 실행 테스트
└── .github/workflows/    # 테스트 → 빌드 → Pages 배포
```

본문의 예제 코드는 `pymdownx.snippets`로 `examples/` 파일을 그대로 삽입합니다. 예제를 고치면 문서도 같이 바뀌고, 테스트가 실제 실행 결과를 확인합니다.

## 사용한 도구와 라이선스

설치된 패키지의 메타데이터와 라이선스 파일로 확인한 내용입니다(2026-11-03 기준). 정확한 조건은 각 프로젝트의 라이선스 원문을 확인하세요.

| 패키지 | 버전 | 라이선스 | 용도 |
|---|---|---|---|
| [MkDocs](https://www.mkdocs.org/) | 1.6.1 | BSD-2-Clause | 정적 사이트 생성 |
| [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) | 9.8.0 | MIT | 테마 (검색, 다크 모드, 코드 복사) |
| [Requests](https://requests.readthedocs.io/) | 2.34.2 | Apache-2.0 | 13장 예제 |
| [Jinja2](https://jinja.palletsprojects.com/) | 3.1.6 | BSD-3-Clause | 14장 예제 |

Material for MkDocs는 빌드할 때 "2027-05-05에 지원이 끝나며 후속 프로젝트는 Zensical"이라는 안내를 출력합니다. 그 전에 후속 도구로 옮길지 검토가 필요합니다.

## 콘텐츠 라이선스

- 문서(`docs/`): [CC BY 4.0](LICENSE-docs.md)
- 코드(`examples/`, `tests/`, 설정 파일): [MIT](LICENSE)

라이선스 선택은 작성자 의도를 적은 것입니다. 회사 업무에서 이 자료를 쓰거나 다른 자료와 섞어 배포할 때는 담당 부서에 확인하세요.

## 기여

오타나 틀린 설명을 발견하면 Issue나 Pull Request로 알려 주세요. 예제를 추가할 때는 `examples/`에 파일을 두고 `tests/test_examples.py`에 실행 확인을 추가해 주세요. 예시 주소에는 `example.com`을 쓰고, 실제 이메일·비밀번호·API 키는 넣지 마세요.
