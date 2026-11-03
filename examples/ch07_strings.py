# 문자열 다루기
s = "  Hello, Python!  "
print(repr(s.strip()))
print(s.strip().lower(), s.strip().upper())
print(s.strip().replace("Python", "파이썬"))
print("Python" in s, s.count("o"))

csv_line = "홍길동,30,서울"
name, age, city = csv_line.split(",")
print(name, int(age) + 1, city)
print("-".join(["2026", "11", "03"]))

# 인덱싱과 슬라이싱
word = "파이썬프로그래밍"
print(word[0], word[-1], word[:3], word[3:], word[::-1])

# 포맷팅
price = 12345.678
print(f"{price:,.2f}원", f"{'왼쪽':<6}|", f"{42:05d}")

# 여러 줄 문자열
poem = """첫째 줄
둘째 줄"""
print(poem.splitlines())
