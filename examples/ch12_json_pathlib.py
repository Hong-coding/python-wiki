# json 과 pathlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
out = base / "_out"
out.mkdir(exist_ok=True)

data = {"name": "민수", "langs": ["Python", "SQL"], "active": True, "score": None}
path = out / "profile.json"
path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

loaded = json.loads(path.read_text(encoding="utf-8"))
print(loaded["langs"], loaded["active"], loaded["score"])
print("파일 이름:", path.name, "확장자:", path.suffix, "부모 폴더:", path.parent.name)

# 폴더 안의 파일 찾기
names = sorted(p.name for p in base.glob("ch0*.py"))
print("ch0 으로 시작하는 예제 수:", len(names))
