# 14. 웹 서버와 HTML 템플릿

13장에서는 **요청을 보내는 쪽**(클라이언트)이었습니다. 이번에는 **요청을 받는 쪽**(서버)을 만들어 봅니다.

## 1분 만에 웹 서버 띄우기

```powershell
cd examples
python -m http.server 8000 --bind 127.0.0.1
```

브라우저에서 <http://127.0.0.1:8000/> 을 열면 현재 폴더의 파일 목록이 보입니다. ++ctrl+c++로 종료합니다. 파이썬에 들어 있는 `http.server` 모듈을 `-m`으로 실행한 것입니다.

## 주소의 의미: 127.0.0.1 과 포트

`http://127.0.0.1:8000/api/hello?name=민수`를 나눠 보면:

| 부분 | 뜻 |
|---|---|
| `http://` | 프로토콜 |
| `127.0.0.1` | 접속할 컴퓨터. **127.0.0.1은 "내 컴퓨터 자신"**을 뜻하는 특별한 주소(루프백)입니다. `localhost`도 같은 뜻입니다. |
| `8000` | 포트. 한 컴퓨터 안에서 여러 서버 프로그램을 구분하는 번호 |
| `/api/hello` | 경로 |
| `?name=민수` | 쿼리 문자열 |

서버가 **127.0.0.1에 바인딩(bind)**하면 같은 컴퓨터에서만 접속할 수 있습니다. `0.0.0.0`에 바인딩하면 같은 네트워크의 다른 컴퓨터도 접속할 수 있게 되므로, 개인 정보를 다루는 로컬 도구는 **127.0.0.1**을 쓰세요.

## 실행해 보기: 나만의 서버

```python title="examples/ch14_http_server.py"
--8<-- "examples/ch14_http_server.py"
```

```powershell
python ch14_http_server.py --port 8000
```

브라우저에서 <http://127.0.0.1:8000/> 과 <http://127.0.0.1:8000/api/hello?name=파이썬> 을 열어 보세요. 두 번째 주소는 HTML이 아니라 **JSON**을 돌려줍니다.

### 코드 읽기

- `BaseHTTPRequestHandler`를 상속한 클래스에서 `do_GET`(GET 요청), `do_POST`(POST 요청) 메서드를 만들면, 요청이 올 때마다 서버가 호출합니다.
- 응답은 **상태 줄 → 헤더 → 빈 줄 → 본문** 순서로 보냅니다. `send_response`, `send_header`, `end_headers`, `wfile.write`가 각각을 담당합니다.
- `Content-Type` 헤더로 본문이 HTML인지 JSON인지 브라우저에 알려 줍니다.
- `LocalServer`는 Windows에서 이미 사용 중인 포트에 서버가 조용히 겹쳐 뜨지 않도록 막는 장치입니다. 자세한 이유는 [사례 학습](18-case-python-m.md#7단계-httpserver로-로컬-웹-서버-띄우기)에서 설명합니다.

!!! warning "http.server 는 학습·로컬 도구용입니다"
    [공식 문서](https://docs.python.org/3/library/http.server.html)는 `http.server`가 **운영(프로덕션) 환경용이 아니며** 기본적인 보안 검사만 한다고 안내합니다. 인터넷에 공개하는 서비스라면 Flask, FastAPI, Django 같은 프레임워크와 제대로 된 웹 서버를 쓰세요.

## HTML 템플릿: Jinja2

HTML을 파이썬 문자열 더하기로 만들면 읽기 어렵고, 사용자 입력에 `<script>`가 섞이면 **XSS(교차 사이트 스크립팅)** 취약점이 생깁니다. 템플릿 엔진 **Jinja2**를 쓰면 HTML 틀과 데이터를 분리할 수 있습니다.

```powershell
python -m pip install Jinja2
```

```html+jinja title="examples/templates/report.html"
--8<-- "examples/templates/report.html"
```

| 문법 | 뜻 |
|---|---|
| `{{ 변수 }}` | 값 출력 (autoescape가 켜져 있으면 `<`→`&lt;` 자동 변환) |
| `{% if %} ... {% endif %}` | 조건 |
| `{% for x in 목록 %} ... {% endfor %}` | 반복 |
| `{{ 값 \| upper }}` | 필터 |

```python title="examples/ch14_jinja.py"
--8<-- "examples/ch14_jinja.py"
```

실행 후 `examples\_out\report.html`을 브라우저로 열어 보세요. 두 번째 항목의 `<script>`가 실행되지 않고 **글자 그대로** 보인다면 autoescape가 제대로 동작한 것입니다.

!!! danger "autoescape 를 끄지 마세요"
    `Environment()`를 그냥 만들면 autoescape가 **꺼져 있습니다.** HTML을 만들 때는 위 예제처럼 `select_autoescape(["html"])`을 꼭 지정하세요. `|safe` 필터는 신뢰할 수 있는 값에만 씁니다.

## 연습문제

1. `ch14_http_server.py`에 `/api/time` 경로를 추가해 현재 시각을 `{"now": "2026-11-03T07:30:00"}` 형태의 JSON으로 돌려주세요.
2. `report.html` 템플릿에 항목 개수를 `총 N건`으로 표시하세요. (힌트: `{{ items | length }}`)

??? success "해답"
    1. `do_GET`의 `elif` 사이에 추가합니다.
       ```python
       elif parts.path == "/api/time":
           from datetime import datetime
           body = json.dumps({"now": datetime.now().isoformat(timespec="seconds")})
           self._send(HTTPStatus.OK, body.encode("utf-8"), "application/json; charset=utf-8")
       ```
    2. `<h1>` 아래에 `<p>총 {{ items | length }}건</p>`을 넣습니다.
