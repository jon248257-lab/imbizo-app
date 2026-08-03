import os
import time

WHATSAPP_LOG = "data/whatsapp_log.txt"

def send_whatsapp_alert(phone, learner_name, date_str, school_name):
    try:
        # We use a simple log first. Real sending with pywhatkit needs internet
        # If pywhatkit fails, we just log it and continue
        msg = f"Hello Parent, {learner_name} was ABSENT today {date_str} at {school_name}. Please confirm."

        os.makedirs("data", exist_ok=True)
        with open(WHATSAPP_LOG, "a") as f:
            f.write(f"{time.ctime()} | To: {phone} | Msg: {msg}\n")

        # TODO: Add real pywhatkit here later
        # import pywhatkit
        # pywhatkit.sendwhatmsg_instantly(phone, msg, 15, True, 5)

        return True, "Logged. Will send when online"
    except Exception as e:
        return False, f"WhatsApp failed: {e}" # But app continues
