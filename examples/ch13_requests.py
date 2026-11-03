# requests 로 웹 페이지/RSS 가져오기
# 실행 예) python ch13_requests.py https://example.com
import sys

import requests

from ch13_rss_parse import parse_rss

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"

try:
    resp = requests.get(
        url,
        headers={"User-Agent": "python-wiki-example/1.0"},
        timeout=10,                      # 응답이 없을 때 무한정 기다리지 않도록
    )
    resp.raise_for_status()              # 4xx/5xx 면 예외 발생
except requests.RequestException as e:
    print("요청 실패:", type(e).__name__, e)
    sys.exit(1)

print("상태 코드:", resp.status_code)
print("Content-Type:", resp.headers.get("Content-Type"))
print("본문 길이:", len(resp.content), "바이트")

if b"<rss" in resp.content[:500]:
    for it in parse_rss(resp.content)[:5]:
        print("-", it["title"])
