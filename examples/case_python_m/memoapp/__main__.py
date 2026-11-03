"""python -m memoapp 으로 실행하면 이 파일이 실행됩니다."""

import sys

from .store import MemoStore, default_path   # 상대 import: 같은 패키지의 store 모듈


def main() -> int:
    print(f"__name__ = {__name__!r}, __package__ = {__package__!r}")
    memos = MemoStore(default_path()).load()
    print(f"메모 {len(memos)}개")
    for m in memos:
        print("-", m["text"])
    print("관리 화면은: python -m memoapp.admin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
