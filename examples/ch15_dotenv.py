# .env 파일을 읽어 환경변수로 넣는 아주 작은 로더 (학습용)
# 실무에서는 python-dotenv 같은 라이브러리를 써도 됩니다.
import os
from pathlib import Path


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)   # 이미 있는 값은 덮어쓰지 않음


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    out = base / "_out"
    out.mkdir(exist_ok=True)
    sample = out / ".env.sample"
    sample.write_text("# 예시 값입니다\nAPP_MODE=dev\nAPI_KEY=\"dummy-key-123\"\n", encoding="utf-8")

    load_dotenv(sample)
    print("APP_MODE =", os.environ.get("APP_MODE"))
    key = os.environ.get("API_KEY", "")
    # 시크릿은 화면·로그에 그대로 찍지 않습니다
    print("API_KEY  =", key[:3] + "***" if key else "(없음)")
