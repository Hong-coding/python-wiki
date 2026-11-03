# 예외 처리
def to_int(text):
    try:
        return int(text)
    except ValueError:
        print(f"'{text}' 는 숫자가 아닙니다")
        return None


print(to_int("12"), to_int("abc"))

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("오류:", type(e).__name__, e)
else:
    print("오류가 없을 때만 실행")
finally:
    print("항상 실행")

try:
    open("없는_파일.txt", encoding="utf-8")
except FileNotFoundError as e:
    print("파일 없음:", e.filename)


# 직접 예외 만들고 던지기
class AgeError(ValueError):
    pass


def check_age(age):
    if age < 0:
        raise AgeError(f"나이는 음수가 될 수 없습니다: {age}")
    return age


try:
    check_age(-1)
except AgeError as e:
    print("잡았습니다:", e)
