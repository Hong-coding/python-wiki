"""메모를 JSON 파일에 저장/불러오기"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path


def default_path() -> Path:
    # 현재 폴더가 아니라 '이 파일 위치' 기준 → 어느 폴더에서 실행해도 같은 파일
    env = os.environ.get("MEMOAPP_DATA")
    return Path(env) if env else Path(__file__).resolve().parent.parent / "memos.json"


class MemoStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.Lock()   # 요청이 동시에 와도 파일이 꼬이지 않도록

    def load(self) -> list[dict]:
        if not self.path.is_file():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def add(self, text: str) -> dict:
        text = text.strip()
        if not text:
            raise ValueError("메모 내용이 비어 있습니다")
        if len(text) > 200:
            raise ValueError("메모는 200자까지 쓸 수 있습니다")
        with self.lock:
            memos = self.load()
            memo = {"text": text, "created": datetime.now().isoformat(timespec="seconds")}
            memos.append(memo)
            self.path.write_text(json.dumps(memos, ensure_ascii=False, indent=2), encoding="utf-8")
        return memo
