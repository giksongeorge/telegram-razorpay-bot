from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔑 Replace with your actual Razorpay monthly plan ID
TARGET_PLAN_ID = "plan_I2znqUcBkZn5U"

# 🔑 Replace with your actual Telegram bot token and group/channel ID
TELEGRAM_BOT_TOKEN = "8944690649:AAEd_hrD8uS3hvmwCKK_tPVrQ767j7r7xiU"
GROUP_ID = -2247522257   # Example: numeric ID for your private group

@app.route("/razorpay-webhook", methods=["POST"])
def razorpay_webhook():
    data = request.get_json(force=True)
    event = data.get("event", "")
    subscription = data.get("subscription", {})
    plan_id = subscription.get("plan_id")

    if plan_id == TARGET_PLAN_ID:
        if event == "subscription.activated":
            customer_id = subscription.get("customer_id")
            telegram_id = get_telegram_id(customer_id)
            add_user_to_group(telegram_id)
            print(f"✅ Activated subscription for {customer_id}, added {telegram_id} to group")

        elif event == "subscription.cancelled":
            customer_id = subscription.get("customer_id")
            telegram_id = get_telegram_id(customer_id)
            remove_user_from_group(telegram_id)
            print(f"❌ Cancelled subscription for {customer_id}, removed {telegram_id} from group")

        else:
            print("ℹ️ Ignored event:", event)
    else:
        print("Ignored other plan:", plan_id)

    return jsonify({"status": "ok"})


# --- Helper functions ---

def get_telegram_id(customer_id):
    """
    Lookup Telegram ID from your DB using Razorpay customer_id.
    For now, return a placeholder until DB integration is ready.
    """
    return 123456789  # Replace with actual lookup logic


def add_user_to_group(telegram_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/inviteChatMember"
    payload = {
        "chat_id": GROUP_ID,
        "user_id": telegram_id
    }
    requests.post(url, json=payload)


def remove_user_from_group(telegram_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/kickChatMember"
    payload = {
        "chat_id": GROUP_ID,
        "user_id": telegram_id
    }
    requests.post(url, json=payload)


# --- Entry point ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)
