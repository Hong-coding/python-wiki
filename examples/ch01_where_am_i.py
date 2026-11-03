# 지금 "현재 폴더"가 어디인지, 이 파일은 어디에 있는지 비교합니다.
import os
from pathlib import Path

print("현재 폴더(cwd):", os.getcwd())
print("이 파일의 폴더:", Path(__file__).resolve().parent)

# 상대 경로는 '현재 폴더' 기준으로 찾습니다.
print("data.txt 가 현재 폴더에 있나요?", Path("data.txt").exists())
# 파일 위치 기준으로 찾으면 어디서 실행해도 같은 파일을 가리킵니다.
here = Path(__file__).resolve().parent
print("파일 기준 경로:", here / "data.txt")
