# argparse: 명령줄 옵션 받기
# 실행 예) python ch12_argparse.py 민수 --times 2 --shout
import argparse

parser = argparse.ArgumentParser(description="인사 프로그램")
parser.add_argument("name", help="인사할 사람 이름")
parser.add_argument("--times", type=int, default=1, help="반복 횟수 (기본 1)")
parser.add_argument("--shout", action="store_true", help="큰 소리로(!)")
args = parser.parse_args()

for _ in range(args.times):
    message = f"안녕하세요, {args.name}님"
    print(message + ("!!!" if args.shout else "."))
