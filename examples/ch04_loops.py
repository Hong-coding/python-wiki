# for: 정해진 묶음을 하나씩 꺼내며 반복
fruits = ["사과", "배", "감"]
for fruit in fruits:
    print(fruit)

# range(시작, 끝) — 끝은 포함하지 않습니다
total = 0
for n in range(1, 11):
    total += n
print("1부터 10까지 합:", total)

# enumerate: 번호와 값을 함께
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)

# while: 조건이 참인 동안 반복
count = 3
while count > 0:
    print("카운트다운", count)
    count -= 1

# break(멈춤)와 continue(건너뜀)
for n in range(10):
    if n % 2 == 0:
        continue
    if n > 7:
        break
    print("홀수", n)
