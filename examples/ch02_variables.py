# 변수와 기본 자료형
name = "파이썬"        # str (문자열)
age = 35               # int (정수)
height = 1.75          # float (실수)
is_student = False     # bool (참/거짓)
nothing = None         # NoneType (값 없음)

print(name, age, height, is_student, nothing)
print(type(name), type(age), type(height), type(is_student), type(nothing))

# 형 변환
text = "42"
number = int(text)
print(number + 8)          # 50
print(str(3.14) + "!")     # 3.14!

# 산술 연산
print(7 / 2, 7 // 2, 7 % 2, 2 ** 10)   # 3.5 3 1 1024

# f-string 으로 값 끼워 넣기
print(f"{name}는 {age}살, 키 {height:.1f}m")
