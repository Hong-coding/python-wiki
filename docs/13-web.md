# 13. requests와 RSS 파싱

## 웹은 "요청과 응답"입니다

브라우저로 웹 페이지를 볼 때 일어나는 일은 이렇습니다.

1. 브라우저(클라이언트)가 서버에 **HTTP 요청**을 보냅니다. 예: `GET https://example.com/`
2. 서버가 **HTTP 응답**을 돌려줍니다. 응답에는 **상태 코드**, **헤더**, **본문**이 들어 있습니다.

| 상태 코드 | 뜻 |
|---|---|
| 200 | 성공 |
| 301 / 302 | 다른 주소로 이동 |
| 400 | 잘못된 요청 |
| 401 / 403 | 인증 필요 / 권한 없음 |
| 404 | 없음 |
| 429 | 요청이 너무 많음 |
| 500 | 서버 오류 |

파이썬 프로그램도 브라우저처럼 요청을 보낼 수 있습니다. 표준 라이브러리 `urllib.request`도 있지만, 보통은 더 쓰기 편한 **requests** 라이브러리를 씁니다.

```powershell
python -m pip install requests
```

## requests 기본

```python
import requests

resp = requests.get("https://example.com", timeout=10)
resp.status_code      # 200
resp.headers["Content-Type"]
resp.text             # 본문 (문자열)
resp.content          # 본문 (바이트)
resp.json()           # 본문이 JSON 이면 파이썬 객체로

# 쿼리 문자열은 params 로 — 한글·특수문자를 알아서 인코딩해 줍니다
requests.get("https://example.com/search", params={"q": "파이썬"}, timeout=10)

# POST 로 JSON 보내기
requests.post("https://example.com/api", json={"name": "민수"}, timeout=10)
```

!!! warning "timeout 은 꼭 지정하세요"
    `timeout`을 주지 않으면 서버가 응답하지 않을 때 **끝없이 기다릴 수** 있습니다. 예약 실행되는 프로그램이 멈춰 버리는 흔한 원인입니다.

!!! note "남의 사이트에서 데이터를 가져올 때"
    - 사이트의 **이용약관과 `robots.txt`**를 확인하고, 공식 API나 RSS가 있으면 그것을 쓰세요.
    - 짧은 시간에 요청을 많이 보내지 마세요. 반복 요청 사이에는 `time.sleep()`으로 간격을 둡니다.
    - API 키가 필요하다면 코드에 적지 말고 환경변수로 받으세요. ([15장](15-email-env.md))

## 실행해 보기: 웹 페이지 가져오기

```python title="examples/ch13_requests.py"
--8<-- "examples/ch13_requests.py"
```

```powershell
python ch13_requests.py https://example.com
```

## RSS란?

RSS는 뉴스·블로그의 **새 글 목록**을 XML 형식으로 제공하는 표준입니다. 화면(HTML)을 긁어 오는 것보다 구조가 안정적이어서 프로그램으로 읽기 좋습니다.

```xml title="examples/data/sample_rss.xml"
--8<-- "examples/data/sample_rss.xml"
```

XML은 `<태그>내용</태그>`가 나무처럼 겹쳐진 구조입니다. `&lt;`, `&amp;`는 각각 `<`, `&`를 뜻하는 표기(엔티티)입니다.

## 실행해 보기: RSS 파싱

표준 라이브러리 `xml.etree.ElementTree`로 읽습니다.

```python title="examples/ch13_rss_parse.py"
--8<-- "examples/ch13_rss_parse.py"
```

| 메서드 | 하는 일 |
|---|---|
| `ET.fromstring(bytes)` | XML을 읽어 최상위 요소를 돌려줌 |
| `root.iter("item")` | 모든 하위 단계에서 `<item>` 찾기 |
| `elem.find("title")` | 바로 아래 자식 하나 |
| `elem.findtext("title", default="")` | 자식의 글자 내용 (없으면 기본값) |
| `elem.get("href")` | 속성 값 |

!!! danger "신뢰할 수 없는 XML"
    표준 `xml` 모듈은 악의적으로 만든 XML(엄청나게 커지는 엔티티 등)에 취약할 수 있다고 [공식 문서](https://docs.python.org/3/library/xml.html#xml-vulnerabilities)가 경고합니다. 출처를 알 수 없는 XML을 다룬다면 `defusedxml` 패키지 사용을 검토하세요.

`pubDate`의 `Mon, 02 Nov 2026 09:00:00 +0900` 형식은 메일 날짜 형식과 같아서 `email.utils.parsedate_to_datetime`으로 바꿀 수 있습니다.

## 연습문제

1. `parse_rss` 결과에서 제목에 "파이썬"이 들어간 항목만 출력하세요.
2. `requests.get`으로 <https://example.com> 을 가져와 HTML의 `<title>` 내용을 출력하세요. (힌트: `text.find("<title>")`)
3. `ch13_requests.py`에 존재하지 않는 주소(예: `https://example.com/no-such-page`)를 주면 어떻게 되나요?

??? success "해답"
    ```python
    # examples 폴더에서 실행
    from pathlib import Path
    from ch13_rss_parse import parse_rss

    items = parse_rss(Path("data/sample_rss.xml").read_bytes())
    for it in items:
        if "파이썬" in it["title"]:
            print(it["title"])
    ```

    ```python title="2번"
    import requests

    html = requests.get("https://example.com", timeout=10).text
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    print(html[start:end])
    ```

    3번: 서버가 404를 돌려주면 `raise_for_status()`가 `HTTPError`를 일으키고, 예제는 `요청 실패: HTTPError ...`를 출력한 뒤 종료 코드 1로 끝납니다.
