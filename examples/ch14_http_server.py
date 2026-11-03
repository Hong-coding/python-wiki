# http.server 로 만드는 아주 작은 웹 서버
# 실행: python ch14_http_server.py  →  브라우저에서 http://127.0.0.1:8000/
import argparse
import json
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGE = """<!doctype html>
<meta charset="utf-8"><title>작은 서버</title>
<h1>안녕하세요!</h1>
<p><a href="/api/hello?name=파이썬">/api/hello</a> 를 눌러 JSON 을 받아 보세요.</p>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body: bytes, content_type: str):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        from urllib.parse import parse_qs, urlsplit

        parts = urlsplit(self.path)
        if parts.path == "/":
            self._send(HTTPStatus.OK, PAGE.encode("utf-8"), "text/html; charset=utf-8")
        elif parts.path == "/api/hello":
            name = parse_qs(parts.query).get("name", ["손님"])[0]
            body = json.dumps({"message": f"{name}님 안녕하세요"}, ensure_ascii=False)
            self._send(HTTPStatus.OK, body.encode("utf-8"), "application/json; charset=utf-8")
        else:
            self._send(HTTPStatus.NOT_FOUND, "없는 페이지".encode("utf-8"), "text/plain; charset=utf-8")


class LocalServer(ThreadingHTTPServer):
    # Windows 에서 이미 사용 중인 포트에 조용히 겹쳐 바인딩되는 것을 막습니다 (본문 설명 참고)
    allow_reuse_address = sys.platform != "win32"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8000)
    args = p.parse_args()
    # 127.0.0.1 = 내 컴퓨터 자신. 다른 컴퓨터에서는 접속할 수 없습니다.
    server = LocalServer(("127.0.0.1", args.port), Handler)
    print(f"서버 시작: http://127.0.0.1:{server.server_address[1]}/  (종료: Ctrl+C)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("종료합니다.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
