"""메모 관리 화면 (로컬 전용 웹 서버)

실행: memoapp 폴더의 '부모 폴더'에서  python -m memoapp.admin [--port 8765]
"""

from __future__ import annotations

import argparse
import json
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .store import MemoStore, default_path   # 상대 import → python -m 으로 실행해야 동작

MAX_BODY = 16 * 1024

PAGE = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><title>메모 관리</title></head>
<body>
<h1>메모 관리</h1>
<form id="f"><input id="t" placeholder="메모 입력" maxlength="200"> <button>추가</button></form>
<p id="msg"></p>
<ul id="list"></ul>
<script>
async function refresh() {
  const res = await fetch("/api/memos");          // (1) 브라우저 → 서버: GET 요청
  const data = await res.json();                  // (4) 서버가 보낸 JSON 을 객체로
  const ul = document.getElementById("list");
  ul.innerHTML = "";
  for (const m of data.memos) {
    const li = document.createElement("li");
    li.textContent = m.text + " (" + m.created + ")";  // textContent: HTML 로 해석하지 않음(XSS 방지)
    ul.appendChild(li);
  }
}
document.getElementById("f").addEventListener("submit", async (e) => {
  e.preventDefault();
  const res = await fetch("/api/memos", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text: document.getElementById("t").value}),
  });
  const data = await res.json();
  document.getElementById("msg").textContent = data.ok ? "저장했습니다" : data.message;
  document.getElementById("t").value = "";
  refresh();
});
refresh();
</script>
</body></html>
"""


def make_handler(store: MemoStore, allowed_hosts: set[str]):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: HTTPStatus, data: dict) -> None:
            # (3) 서버 → 브라우저: 파이썬 dict 를 JSON 문자열로 바꿔 보냄
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self._send(status, body, "application/json; charset=utf-8")

        def _host_ok(self) -> bool:
            # 다른 사이트가 주소를 바꿔 접근하는 공격(DNS rebinding)을 막는 간단한 확인
            return self.headers.get("Host", "") in allowed_hosts

        def do_GET(self):
            if not self._host_ok():
                return self._send(HTTPStatus.FORBIDDEN, b"forbidden", "text/plain")
            if self.path == "/":
                return self._send(HTTPStatus.OK, PAGE.encode("utf-8"), "text/html; charset=utf-8")
            if self.path == "/api/memos":
                return self._json(HTTPStatus.OK, {"ok": True, "memos": store.load()})
            self._send(HTTPStatus.NOT_FOUND, b"not found", "text/plain")

        def do_POST(self):
            if not self._host_ok() or self.path != "/api/memos":
                return self._send(HTTPStatus.FORBIDDEN, b"forbidden", "text/plain")
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                return self._json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"ok": False, "message": "JSON 만 받습니다"})
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_BODY:
                return self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"ok": False, "message": "요청이 너무 큽니다"})
            # (2) 브라우저가 보낸 JSON 문자열 → 파이썬 dict
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
                memo = store.add(str(body.get("text", "")))
            except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
                return self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "message": "JSON 형식 오류"})
            except ValueError as e:
                return self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "message": str(e)})
            self._json(HTTPStatus.OK, {"ok": True, "memo": memo})

        def log_message(self, fmt, *args):
            sys.stderr.write(f"[admin] {self.command} {self.path}\n")   # 본문 내용은 기록하지 않음

    return Handler


class LocalServer(ThreadingHTTPServer):
    # Windows 에서는 SO_REUSEADDR 를 켜면 이미 다른 프로그램이 쓰는 포트에도 조용히 바인딩됩니다.
    # 그러면 브라우저가 엉뚱한 서버에 접속할 수 있으므로, 포트가 사용 중이면 오류가 나도록 끕니다.
    allow_reuse_address = sys.platform != "win32"


def create_server(port: int, data_path: Path) -> ThreadingHTTPServer:
    server = LocalServer(("127.0.0.1", port), None)
    real_port = server.server_address[1]   # port=0 이면 운영체제가 빈 포트를 골라 줌
    hosts = {f"127.0.0.1:{real_port}", f"localhost:{real_port}"}
    server.RequestHandlerClass = make_handler(MemoStore(data_path), hosts)
    return server


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="memoapp.admin", description="메모 관리 화면")
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args(argv)

    server = create_server(args.port, default_path())
    print(f"메모 관리 화면: http://127.0.0.1:{server.server_address[1]}/  (종료: Ctrl+C)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n종료합니다.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
