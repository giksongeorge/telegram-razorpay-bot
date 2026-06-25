from flask import Flask, request
import telegram
import razorpay

app = Flask(__name__)

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GROUP_ID = -123456789  # Telegram group/channel ID
bot = telegram.Bot(token=TELEGRAM_TOKEN)

razorpay_client = razorpay.Client(auth=("RAZORPAY_KEY", "RAZORPAY_SECRET"))

@app.route("/razorpay-webhook", methods=["POST"])
def razorpay_webhook():
    data = request.json
    event = data.get("event")

    # Example: subscription activated
    if event == "subscription.activated":
        customer_id = data["payload"]["subscription"]["entity"]["customer_id"]
        telegram_id = get_telegram_id(customer_id)  # lookup from DB
        bot.invite_chat_member(chat_id=GROUP_ID, user_id=telegram_id)

    # Example: subscription cancelled
    elif event == "subscription.cancelled":
        customer_id = data["payload"]["subscription"]["entity"]["customer_id"]
        telegram_id = get_telegram_id(customer_id)
        bot.kick_chat_member(chat_id=GROUP_ID, user_id=telegram_id)

    return "ok", 200
