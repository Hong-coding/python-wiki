# greet 를 import 하면 greet.py 의 맨 위부터 실행되지만, if __name__ == "__main__" 블록은 건너뜁니다.
import greet

print(greet.hello("import 한 쪽"))
print(f"use_greet.py 의 __name__ = {__name__!r}")
