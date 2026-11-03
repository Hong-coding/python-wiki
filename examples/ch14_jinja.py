# Jinja2 로 HTML 만들기 (pip install Jinja2)
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

base = Path(__file__).resolve().parent
env = Environment(
    loader=FileSystemLoader(base / "templates"),
    autoescape=select_autoescape(["html"]),   # <, > 같은 문자를 안전하게 바꿔 XSS 를 막습니다
)
template = env.get_template("report.html")

items = [
    {"title": "파이썬 입문", "url": "https://example.com/1", "views": 150},
    {"title": "<script>alert(1)</script>", "url": "https://example.com/2", "views": 3},
]
html = template.render(title="오늘의 글", day="2026-11-03", items=items)

out = base / "_out"
out.mkdir(exist_ok=True)
(out / "report.html").write_text(html, encoding="utf-8")
print("저장:", (out / "report.html").name)
print("이스케이프 확인:", "&lt;script&gt;" in html)
