# afisha_checker.py (одноразовая проверка)
import requests
import hashlib
import os

URL = 'https://puppet-minsk.by/afisha'
HASH_FILE = 'last_hash.txt'
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

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
    payload = {'chat_id': CHAT_ID, 'text': text}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Ошибка отправки сообщения:", e)

def load_last_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return f.read().strip()
    return ''

def save_hash(hash):
    with open(HASH_FILE, 'w') as f:
        f.write(hash)

def main():
    current_hash = get_page_hash()
    if not current_hash:
        return
    last_hash = load_last_hash()
    if current_hash != last_hash:
        send_telegram_message("🎭 Афиша театра обновилась! https://puppet-minsk.by/afisha")
        save_hash(current_hash)
    else:
        print("Без изменений.")

if __name__ == '__main__':
    main()
