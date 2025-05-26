import requests
import hashlib
import time

# Настройки
URL = 'https://puppet-minsk.by/afisha'
CHECK_INTERVAL = 3600  # раз в час (в секундах)
BOT_TOKEN = '8174740820:AAEW2hGlPpMkGdn_EfkTkA3or8apDiXh_Xc'
CHAT_ID = '840546514'

def get_page_hash():
    try:
        response = requests.get(URL, timeout=10)
        content = response.text
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    except Exception as e:
        print("Ошибка при получении страницы:", e)
        return None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Ошибка отправки сообщения:", e)

def main():
    last_hash = get_page_hash()
    if not last_hash:
        print("Ошибка при первом запуске.")
        return

    print("Начинаю отслеживание афиши...")

    while True:
        time.sleep(CHECK_INTERVAL)
        current_hash = get_page_hash()
        if not current_hash:
            continue

        if current_hash != last_hash:
            print("Обнаружено обновление!")
            send_telegram_message("🎭 Афиша театра обновилась! Проверь здесь: https://puppet-minsk.by/afisha")
            last_hash = current_hash
        else:
            print("Афиша не изменилась.")

if __name__ == '__main__':
    main()
