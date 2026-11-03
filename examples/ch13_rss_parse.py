# RSS(XML) 파싱: 표준 라이브러리 xml.etree.ElementTree 사용
import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path


def parse_rss(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.iter("item"):                       # 모든 <item> 태그
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        pub = item.findtext("pubDate")
        when = parsedate_to_datetime(pub) if pub else None
        items.append({"title": title, "link": link, "when": when})
    return items


if __name__ == "__main__":
    # 인자가 없으면 이 파일 옆 data/sample_rss.xml 을 읽습니다
    default = Path(__file__).resolve().parent / "data" / "sample_rss.xml"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    for i, it in enumerate(parse_rss(path.read_bytes()), start=1):
        when = it["when"].strftime("%Y-%m-%d %H:%M") if it["when"] else "-"
        print(f"{i}. [{when}] {it['title']} ({it['link']})")
