# ch10_modules 폴더에서 실행: python main.py
import math                      # 표준 라이브러리
from pathlib import Path

import calc                      # 우리가 만든 패키지 (calc 폴더)
import calc.ops as ops
from calc import add, multiply

print(add(2, 3), multiply(4, 5), ops.add(1, 1))
print(math.sqrt(16), round(math.pi, 4))
print("calc 패키지 파일:", Path(calc.__file__).parent.name + "/" + Path(calc.__file__).name)
print("이 파일의 __name__:", __name__)
