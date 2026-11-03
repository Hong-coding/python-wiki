"""문서의 연습문제 해답 코드가 실제로 실행되는지 확인하는 테스트

대상: docs/*.md 의 '??? success "해답"' 블록 안에 있는, 제목(title) 없는 ```python 블록
제외: input() 을 쓰는 코드, 제목이 붙은 코드(파일 일부·네트워크 예제 등)
"""

import os
import re
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
EXAMPLES = ROOT / "examples"

# 해답 블록 안(4칸 들여쓰기)의 제목 없는 python 코드 블록
BLOCK = re.compile(r"^    ```python\n(.*?)^    ```$", re.S | re.M)


def answer_sections(text: str):
    """'??? success' 로 시작해 들여쓰기가 끝날 때까지를 잘라 냅니다."""
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        if lines[i].startswith("??? success"):
            j = i + 1
            while j < len(lines) and (lines[j].startswith("    ") or not lines[j].strip()):
                j += 1
            yield "".join(lines[i + 1:j])
            i = j
        else:
            i += 1


def collect():
    for md in sorted(DOCS.glob("*.md")):
        for section in answer_sections(md.read_text(encoding="utf-8")):
            for m in BLOCK.finditer(section):
                code = textwrap.dedent(m.group(1))
                if "input(" in code:
                    continue
                yield md.name, code


class DocAnswersTest(unittest.TestCase):
    def test_answers_run(self):
        blocks = list(collect())
        self.assertGreaterEqual(len(blocks), 8)
        env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
        for name, code in blocks:
            with self.subTest(doc=name, code=code.splitlines()[0]):
                r = subprocess.run([sys.executable, "-c", code], cwd=EXAMPLES, env=env,
                                   capture_output=True, text=True, encoding="utf-8", timeout=60)
                self.assertEqual(r.returncode, 0, f"{name}\n{code}\n{r.stderr}")
                self.assertNotIn("FAILED", r.stderr)


if __name__ == "__main__":
    unittest.main()
