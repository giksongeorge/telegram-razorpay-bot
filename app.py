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
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace this with the exact Plan ID you copied from Razorpay
TARGET_PLAN_ID = "plan_T2znqUUcBkZn5U"

@app.route("/razorpay-webhook", methods=["POST"])
def razorpay_webhook():
    data = request.get_json()

    subscription = data.get("subscription", {})
    plan_id = subscription.get("plan_id")

    if plan_id == TARGET_PLAN_ID:
        # ✅ This is the monthly subscription plan we care about
        print("Valid subscription event for monthly plan:", plan_id)
        # TODO: Add Telegram bot logic here (e.g., add user to channel)
    else:
        # ❌ Ignore other plans or payment links
        print("Ignored event for plan:", plan_id)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

