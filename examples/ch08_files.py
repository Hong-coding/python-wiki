# 파일 쓰기와 읽기 (항상 encoding="utf-8" 을 적습니다)
from pathlib import Path

out_dir = Path(__file__).resolve().parent / "_out"
out_dir.mkdir(exist_ok=True)
path = out_dir / "memo.txt"

with open(path, "w", encoding="utf-8") as f:
    f.write("첫째 줄\n")
    f.write("둘째 줄\n")

with open(path, "a", encoding="utf-8") as f:   # a: 이어 쓰기
    f.write("셋째 줄\n")

with open(path, encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(number, line.rstrip("\n"))

# pathlib 의 간단한 방법
text = path.read_text(encoding="utf-8")
print("글자 수:", len(text), "줄 수:", len(text.splitlines()))
