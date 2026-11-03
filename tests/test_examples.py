"""위키의 예제 코드가 실제로 실행되는지 확인하는 테스트

실행 (저장소 최상위 폴더에서):  python -m unittest discover -s tests -v
"""

import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EX = ROOT / "examples"
CASE = EX / "case_python_m"


def run(args, cwd=EX, stdin=None, env_extra=None, check=True):
    """예제를 별도 프로세스로 실행하고 결과(CompletedProcess)를 돌려줍니다."""
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    env.update(env_extra or {})
    result = subprocess.run(
        [sys.executable, *args], cwd=cwd, input=stdin, env=env,
        capture_output=True, text=True, encoding="utf-8", timeout=60,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"{args} 실패 ({result.returncode})\n{result.stdout}\n{result.stderr}")
    return result


class BasicExamplesTest(unittest.TestCase):
    # (파일, 출력에 반드시 들어 있어야 할 문자열들)
    CASES = [
        ("ch01_where_am_i.py", ["현재 폴더(cwd):", "파일 기준 경로:"]),
        ("ch02_variables.py", ["50", "3.14!", "3.5 3 1 1024", "파이썬는 35살, 키 1.8m"]),
        ("ch03_conditions.py", ["95 -> A", "40 -> F", "입장 가능", "0 거짓", "'a' 참"]),
        ("ch04_loops.py", ["1부터 10까지 합: 55", "3 감", "카운트다운 1", "홀수 7"]),
        ("ch05_functions.py", ["안녕하세요, 민수님!", "반갑습니다, 지은님!", "1 9", "12", "카운터: 2"]),
        ("ch06_collections.py", ["[70, 80, 88, 95] 4 70 95 [80, 88]", "{'사과': 3, '배': 2, '감': 1}"]),
        ("ch07_strings.py", ["'Hello, Python!'", "홍길동 31 서울", "2026-11-03", "12,345.68원", "00042"]),
        ("ch08_files.py", ["1 첫째 줄", "3 셋째 줄", "줄 수: 3"]),
        ("ch09_exceptions.py", ["'abc' 는 숫자가 아닙니다", "ZeroDivisionError", "항상 실행", "잡았습니다:"]),
        ("ch11_classes.py", ["BankAccount('민수', 1000)", "BankAccount('지은', 10500)", "같은 값인가요? True", "['B', 'A']"]),
        ("ch12_json_pathlib.py", ["['Python', 'SQL'] True None", "확장자: .json"]),
        ("ch12_datetime.py", ["2026-01-01 2026-01-01 3", "100일 뒤: 2026-04-11", "2026-11-03 07:30 KST",
                              "2026-11-02T22:30:00+00:00", "날짜 차이: 52 일", "True"]),
        ("ch12_subprocess.py", ["반환 코드: 0", "자식 프로세스에서 인사", "실패한 반환 코드: 3"]),
        ("ch13_rss_parse.py", ["1. [2026-11-02 09:00] 파이썬 3.13 새 기능 정리", "<초보> 반복문 & 조건문"]),
        ("ch14_jinja.py", ["저장: report.html", "이스케이프 확인: True"]),
        ("ch15_dotenv.py", ["APP_MODE = dev", "API_KEY  = dum***"]),
        ("ch15_email.py", ["미리보기", "To: you@example.com", "['text/plain', 'text/html']"]),
    ]

    def test_examples(self):
        for script, expected in self.CASES:
            with self.subTest(script=script):
                out = run([script]).stdout
                for text in expected:
                    self.assertIn(text, out, f"{script} 출력에 {text!r} 가 없습니다\n{out}")

    def test_ch01_relative_path_depends_on_cwd(self):
        # 같은 파일이라도 '어디서' 실행하느냐에 따라 현재 폴더가 달라집니다
        out_root = run([str(EX / "ch01_where_am_i.py")], cwd=ROOT).stdout
        out_ex = run(["ch01_where_am_i.py"], cwd=EX).stdout
        self.assertIn(str(ROOT), out_root)
        self.assertNotEqual(out_root.splitlines()[0], out_ex.splitlines()[0])

    def test_ch10_modules(self):
        out = run(["main.py"], cwd=EX / "ch10_modules").stdout
        self.assertIn("5 20 2", out)
        self.assertIn("calc/__init__.py", out)
        self.assertIn("__main__", out)
        out = run(["-m", "calc.ops"], cwd=EX / "ch10_modules").stdout
        self.assertIn("ops 모듈 단독 실행: 5", out)

    def test_ch12_argparse(self):
        out = run(["ch12_argparse.py", "민수", "--times", "2", "--shout"]).stdout
        self.assertEqual(out.count("안녕하세요, 민수님!!!"), 2)
        bad = run(["ch12_argparse.py"], check=False)
        self.assertEqual(bad.returncode, 2)   # 필수 인자 누락 → argparse 가 2로 종료

    def test_ch16_unittest(self):
        r = run(["-m", "unittest", "-v"], cwd=EX / "ch16_testing")
        self.assertIn("OK", r.stderr)


class LocalServerMixin:
    """테스트용으로 examples/data 폴더를 서빙하는 로컬 웹 서버"""

    @classmethod
    def setUpClass(cls):
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass

        handler = partial(QuietHandler, directory=str(EX / "data"))
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()


class RequestsExampleTest(LocalServerMixin, unittest.TestCase):
    def test_fetch_rss(self):
        out = run(["ch13_requests.py", f"{self.base}/sample_rss.xml"]).stdout
        self.assertIn("상태 코드: 200", out)
        self.assertIn("- 가상환경을 꼭 써야 하는 이유", out)

    def test_404(self):
        r = run(["ch13_requests.py", f"{self.base}/none.xml"], check=False)
        self.assertEqual(r.returncode, 1)
        self.assertIn("요청 실패: HTTPError", r.stdout)


def http(method, url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


class Ch14ServerTest(unittest.TestCase):
    def test_server(self):
        sys.path.insert(0, str(EX))
        try:
            import ch14_http_server as mod
        finally:
            sys.path.remove(str(EX))
        server = ThreadingHTTPServer(("127.0.0.1", 0), mod.Handler)
        server.RequestHandlerClass.log_message = lambda *a: None
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            status, body = http("GET", base + "/")
            self.assertEqual(status, 200)
            self.assertIn("안녕하세요!", body)
            status, body = http("GET", base + "/api/hello?name=%EB%AF%BC%EC%88%98")
            self.assertEqual(json.loads(body), {"message": "민수님 안녕하세요"})
            status, _ = http("GET", base + "/nope")
            self.assertEqual(status, 404)
        finally:
            server.shutdown()
            server.server_close()


class CaseStudyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data = Path(self.tmp.name) / "memos.json"
        self.env = {"MEMOAPP_DATA": str(self.data)}

    def tearDown(self):
        self.tmp.cleanup()

    def test_python_m_package(self):
        out = run(["-m", "memoapp"], cwd=CASE, env_extra=self.env).stdout
        self.assertIn("__name__ = '__main__', __package__ = 'memoapp'", out)
        self.assertIn("메모 0개", out)

    def test_direct_run_fails_with_relative_import(self):
        # python memoapp/admin.py 처럼 파일 경로로 실행하면 상대 import 가 실패합니다
        r = run(["memoapp/admin.py"], cwd=CASE, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ImportError", r.stderr)

    def test_wrong_folder_fails(self):
        # memoapp 폴더 '안'에서 python -m memoapp.admin → 패키지를 찾지 못함
        r = run(["-m", "memoapp.admin"], cwd=CASE / "memoapp", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("No module named 'memoapp'", r.stderr)

    def test_name_main(self):
        out = run(["greet.py"], cwd=CASE).stdout
        self.assertIn("greet.py 의 __name__ = '__main__'", out)
        self.assertIn("안녕하세요, 직접 실행님", out)
        out = run(["use_greet.py"], cwd=CASE).stdout
        self.assertIn("greet.py 의 __name__ = 'greet'", out)
        self.assertNotIn("직접 실행", out)

    def test_admin_server_json_flow(self):
        sys.path.insert(0, str(CASE))
        try:
            from memoapp.admin import create_server
        finally:
            sys.path.remove(str(CASE))
        server = create_server(0, self.data)
        server.RequestHandlerClass.log_message = lambda *a: None
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        js = {"Content-Type": "application/json"}
        try:
            status, body = http("GET", base + "/")
            self.assertEqual(status, 200)
            self.assertIn("메모 관리", body)
            status, body = http("POST", base + "/api/memos", json.dumps({"text": "우유 사기"}).encode(), js)
            self.assertEqual(status, 200)
            self.assertTrue(json.loads(body)["ok"])
            status, body = http("GET", base + "/api/memos")
            self.assertEqual([m["text"] for m in json.loads(body)["memos"]], ["우유 사기"])
            status, body = http("POST", base + "/api/memos", json.dumps({"text": "  "}).encode(), js)
            self.assertEqual(status, 400)
            status, _ = http("POST", base + "/api/memos", b"text=1", {"Content-Type": "text/plain"})
            self.assertEqual(status, 415)
            status, _ = http("GET", base + "/api/memos", headers={"Host": "evil.example.com"})
            self.assertEqual(status, 403)
        finally:
            server.shutdown()
            server.server_close()

    def test_port_in_use_raises(self):
        # 이미 사용 중인 포트로 띄우면 (Windows 포함) OSError 가 나야 합니다
        sys.path.insert(0, str(CASE))
        try:
            from memoapp.admin import create_server
        finally:
            sys.path.remove(str(CASE))
        first = create_server(0, self.data)
        try:
            with self.assertRaises(OSError):
                create_server(first.server_address[1], self.data).server_close()
        finally:
            first.server_close()

    def test_admin_starts_via_python_m(self):
        # 실제로 python -m memoapp.admin --port 0 을 띄워 첫 줄 안내가 나오는지 확인
        env = {**os.environ, "PYTHONUTF8": "1", **self.env}
        proc = subprocess.Popen([sys.executable, "-m", "memoapp.admin", "--port", "0"], cwd=CASE, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        try:
            line = proc.stdout.readline()
            self.assertIn("메모 관리 화면: http://127.0.0.1:", line)
        finally:
            proc.kill()
            proc.communicate(timeout=10)


if __name__ == "__main__":
    unittest.main()
