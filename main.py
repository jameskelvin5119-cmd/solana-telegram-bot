import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return jsonify({"status": "no data"}), 200

    for event in data:
        tx = event.get("signature", "N/A")
        description = event.get("description", "New Solana transaction detected")

        message = (
            "🚨 <b>Solana Wallet Activity</b>\n\n"
            f"{description}\n\n"
            f"<b>Tx:</b> {tx}"
        )

        send_telegram(message)

    return jsonify({"status": "ok"}), 200

@app.route("/", methods=["GET"])
def health():
    return "Bot is running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
