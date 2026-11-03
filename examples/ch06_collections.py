# 리스트: 순서가 있는 묶음
scores = [80, 95, 70]
scores.append(88)
scores.sort()
print(scores, len(scores), scores[0], scores[-1], scores[1:3])

# 리스트 컴프리헨션
squares = [n * n for n in range(1, 6)]
evens = [n for n in range(10) if n % 2 == 0]
print(squares, evens)

# 딕셔너리: 키 → 값
person = {"name": "민수", "age": 30}
person["city"] = "서울"
print(person["name"], person.get("email", "(없음)"))
for key, value in person.items():
    print(key, "=", value)

# 단어 수 세기
words = "사과 배 사과 감 배 사과".split()
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)

# 튜플과 집합
point = (3, 4)
unique = set(words)
print(point, sorted(unique))
