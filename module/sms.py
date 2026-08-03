import json
import os
from datetime import datetime

try:
    from android.sms import SMS # Only works on Android
    ANDROID = True
except:
    ANDROID = False

SMS_QUEUE_FILE = "data/sms_queue.json"
SMS_SETTINGS_FILE = "data/sms_settings.kr"
SMS_COST = 200 # UGX per SMS. User can change

class SMSHandler:
    @staticmethod
    def load_settings():
        if not os.path.exists(SMS_SETTINGS_FILE):
            return {"sms_enabled": False, "sender_name": "School", "balance": 5000}
        with open(SMS_SETTINGS_FILE, "r") as f:
            parts = f.read().split(",")
            return {"sms_enabled": parts[0]=="1", "sender_name": parts[1], "balance": int(parts[2])}

    @staticmethod
    def save_settings(enabled, sender, balance):
        os.makedirs("data", exist_ok=True)
        with open(SMS_SETTINGS_FILE, "w") as f:
            f.write(f"{1 if enabled else 0},{sender},{balance}")

    @staticmethod
    def send_sms(phone, message):
        if not ANDROID:
            return False, "SMS only works on Android phone"
        try:
            sms = SMS()
            sms.send(phone, message)
            return True, "SMS Sent"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def add_to_queue(phone, message):
        queue = []
        if os.path.exists(SMS_QUEUE_FILE):
            with open(SMS_QUEUE_FILE, "r") as f:
                queue = json.load(f)
        queue.append({"phone": phone, "message": message, "time": str(datetime.now())})
        with open(SMS_QUEUE_FILE, "w") as f:
            json.dump(queue, f)

    @staticmethod
    def process_queue():
        settings = SMSHandler.load_settings()
        if not settings["sms_enabled"] or settings["balance"] < SMS_COST:
            return 0

        if not os.path.exists(SMS_QUEUE_FILE):
            return 0

        with open(SMS_QUEUE_FILE, "r") as f:
            queue = json.load(f)

        sent = 0
        new_queue = []
        for item in queue:
            if settings["balance"] >= SMS_COST:
                success, _ = SMSHandler.send_sms(item["phone"], item["message"])
                if success:
                    settings["balance"] -= SMS_COST
                    sent += 1
                else:
                    new_queue.append(item) # keep failed ones

        with open(SMS_QUEUE_FILE, "w") as f:
            json.dump(new_queue, f)
        SMSHandler.save_settings(settings["sms_enabled"], settings["sender_name"], settings["balance"])
        return sent
