import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# =========================
# Environment variables
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# =========================
# Send message to Telegram
# =========================
def send_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not set")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    requests.post(url, json=payload)


# =========================
# Helius Webhook Endpoint
# =========================
@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return jsonify({"status": "no data"}), 200

    # Helius sends a single JSON object
    tx = data.get("signature", "N/A")
    description = data.get("description", "New Solana transaction detected")

    message = (
        "🔔 <b>Solana Wallet Activity</b>\n\n"
        f"{description}\n\n"
        f"<b>Tx:</b> {tx}"
    )

    send_telegram(message)

    return jsonify({"status": "ok"}), 200


# =========================
# Health Check (Render)
# =========================
@app.route("/", methods=["GET"])
def health():
    return "Bot is running", 200


# =========================
# App start
# =========================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
