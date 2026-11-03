# datetime: 날짜와 시간
from datetime import date, datetime, timedelta, timezone

KST = timezone(timedelta(hours=9), "KST")   # 한국 표준시 (UTC+9)

d = date(2026, 1, 1)
print(d, d.isoformat(), d.weekday())          # weekday: 월=0 ... 일=6
print("100일 뒤:", d + timedelta(days=100))

dt = datetime(2026, 11, 3, 7, 30, tzinfo=KST)
print(dt.strftime("%Y-%m-%d %H:%M"), dt.tzname())
print("UTC로:", dt.astimezone(timezone.utc).isoformat())

parsed = datetime.strptime("2026-03-01 09:00", "%Y-%m-%d %H:%M")
print("문자열→날짜:", parsed.year, parsed.month, parsed.day)
print("날짜 차이:", (date(2026, 12, 25) - date(2026, 11, 3)).days, "일")

now = datetime.now(KST)   # 실행할 때마다 달라집니다
print("지금 연도는 4자리:", len(str(now.year)) == 4)
