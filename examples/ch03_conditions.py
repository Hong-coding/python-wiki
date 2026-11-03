# 점수에 따라 학점 매기기
def grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"


for s in [95, 85, 72, 40]:
    print(s, "->", grade(s))

# and / or / not 과 비교 연산
age = 20
has_ticket = True
if age >= 19 and has_ticket:
    print("입장 가능")
if not has_ticket:
    print("표가 없습니다")

# 빈 값은 거짓으로 취급됩니다 (truthy / falsy)
for value in [0, "", [], None, 1, "a"]:
    print(repr(value), "참" if value else "거짓")
