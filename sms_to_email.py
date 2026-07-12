"""
Автоматическая пересылка входящих SMS на email
Требует Android с Python (Termux или QPython)
"""

import smtplib
from email.mime.text import MIMEText
import json
import time

# Настройки
CONFIG = {
    "email": "<your_email@gmail.com>",
    "password": "<app_password>",  # Пароль приложения Gmail
    "forward_to": "<recipient@example.com>"
}


def send_email(sender, message, timestamp):
    """Отправляет SMS на email"""
    msg = MIMEText(f"От: {sender}\nВремя: {timestamp}\n\n{message}", "plain", "utf-8")
    msg["Subject"] = f"SMS от {sender}"
    msg["From"] = CONFIG["email"]
    msg["To"] = CONFIG["forward_to"]
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(CONFIG["email"], CONFIG["password"])
        server.send_message(msg)


def read_last_sms():
    """Читает последнее SMS (для Android через Termux)"""
    try:
        # Termux API
        import subprocess
        result = subprocess.run(
            ["termux-sms-list", "-l", "1"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data:
                return data[0]
    except:
        pass
    return None


def main():
    """Основной цикл мониторинга"""
    processed = set()
    
    print("Запущен мониторинг SMS...")
    while True:
        sms = read_last_sms()
        if sms:
            sms_id = sms.get("_id")
            if sms_id not in processed:
                print(f"Новое SMS от {sms['number']}")
                send_email(
                    sms.get("number"),
                    sms.get("body"),
                    sms.get("received")
                )
                processed.add(sms_id)
        
        time.sleep(10)


if __name__ == "__main__":
    main()
