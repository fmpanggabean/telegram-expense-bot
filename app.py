from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = '7787446939:AAGBNAtRoodl7J0XTILCu7lbgpZ-axJtgCg'
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzk4d9Hm_rcy3GCiVv5glpjuNSHAqhcvZpJbXgwEeIf2FfQEAMA-yJE8BisiW8ac0o/exec'

def parse_message(text, sender_name):
    try:
        parts = text.split(',')
        return {
            'name': sender_name,
            'category': parts[0].strip(),
            'amount': float(parts[1].strip()),
            'note': parts[2].strip() if len(parts) > 2 else ''
        }
    except Exception:
        return None

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if 'message' in data:
        msg = data['message']
        text = msg.get('text')
        sender_name = msg['from'].get('first_name', 'Unknown')

        parsed = parse_message(text, sender_name)
        if parsed:
            requests.post(GOOGLE_SCRIPT_URL, json=parsed)
            reply = "✅ Pengeluaran dicatat!"
        else:
            reply = "⚠️ Format salah. Gunakan: kategori, jumlah, catatan"

        chat_id = msg['chat']['id']
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={'chat_id': chat_id, 'text': reply}
        )

    return "OK"
