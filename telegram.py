import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_alert(signal, risk):
    text = f"""
🚀 *SUPERSTAR SCALP ALERT*

🪙 Coin: *{signal['symbol']}*
📊 Rating: *{signal['score']}/10*
📈 Trend: *{signal['trend']}*

💰 Entry: {risk['entry']}
🛑 Stop Loss: {risk['stop_loss']}
🎯 Book Profit: {risk['target']}
⚡ Leverage: {risk['leverage']}

🧠 Reason:
{", ".join(signal['reasons'])}
{risk['reason']}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })
