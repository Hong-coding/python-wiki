# subprocess: 다른 프로그램 실행하기
import subprocess
import sys

# sys.executable = 지금 실행 중인 파이썬 (가상환경이면 가상환경의 파이썬)
result = subprocess.run(
    [sys.executable, "-c", "print('자식 프로세스에서 인사')"],
    capture_output=True, text=True, encoding="utf-8", check=True,
)
print("반환 코드:", result.returncode)
print("출력:", result.stdout.strip())

# 실패하는 명령: check=True 면 예외가 납니다
try:
    subprocess.run([sys.executable, "-c", "import sys; sys.exit(3)"], check=True)
except subprocess.CalledProcessError as e:
    print("실패한 반환 코드:", e.returncode)
