# 이 파일을 직접 실행할 때와 import 할 때 __name__ 이 다릅니다.
def hello(name):
    return f"안녕하세요, {name}님"


print(f"greet.py 의 __name__ = {__name__!r}")

if __name__ == "__main__":
    # python greet.py 로 '직접' 실행했을 때만 여기가 실행됩니다
    print(hello("직접 실행"))
