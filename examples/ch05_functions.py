# 함수 정의와 호출
def greet(name, greeting="안녕하세요"):
    """인사말을 만들어 돌려줍니다."""
    return f"{greeting}, {name}님!"


print(greet("민수"))
print(greet("지은", greeting="반갑습니다"))


# 여러 값 돌려주기 (튜플)
def min_max(numbers):
    return min(numbers), max(numbers)


low, high = min_max([3, 9, 1, 7])
print(low, high)


# 가변 인자
def total(*numbers, **options):
    result = sum(numbers)
    if options.get("double"):
        result *= 2
    return result


print(total(1, 2, 3))
print(total(1, 2, 3, double=True))

# 지역 변수는 함수 밖에서 보이지 않습니다
def make_counter():
    count = 0
    def increase():
        nonlocal count
        count += 1
        return count
    return increase


counter = make_counter()
counter()
print("카운터:", counter())
