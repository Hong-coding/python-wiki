# smtplib 로 메일 보내기
# 기본은 미리보기만 하고, --send 를 붙여야 실제로 보냅니다.
#   필요한 환경변수: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, MAIL_TO
import argparse
import os
import smtplib
import ssl
from email.message import EmailMessage


def build_message(sender: str, to: list[str], subject: str, text: str, html: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject
    msg.set_content(text)                      # 일반 텍스트 본문
    msg.add_alternative(html, subtype="html")  # HTML 본문 (지원하는 메일 앱은 이쪽을 표시)
    return msg


def send(msg: EmailMessage) -> None:
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]    # 코드에 비밀번호를 쓰지 않습니다
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls(context=ssl.create_default_context())   # 암호화
        smtp.login(user, password)
        smtp.send_message(msg)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--send", action="store_true", help="실제로 발송")
    args = p.parse_args()

    sender = os.environ.get("SMTP_USER", "me@example.com")
    to = [a.strip() for a in os.environ.get("MAIL_TO", "you@example.com").split(",") if a.strip()]
    msg = build_message(sender, to, "테스트 메일", "안녕하세요. 텍스트 본문입니다.",
                        "<h1>안녕하세요</h1><p>HTML 본문입니다.</p>")
    if args.send:
        send(msg)
        print(f"발송 완료: {len(to)}명")
    else:
        print("미리보기 (발송하지 않음)")
        print("From:", msg["From"])
        print("To:", msg["To"])
        print("Subject:", msg["Subject"])
        print("본문 종류:", [part.get_content_type() for part in msg.iter_parts()])
