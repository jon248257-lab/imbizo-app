import hashlib
import json
import os
from datetime import datetime

LICENSE_FILE = "data/subscription.lic"
SECRET_KEY = "KAMPALA_SCHOOL_ATTENDANCE_2026_XYZ" # Change this. Keep it secret

class Subscription:
    @staticmethod
    def generate_code(school_name, year, month):
        """You will use this on YOUR computer to generate code for customer"""
        raw = f"{school_name}{year}{month:02d}{SECRET_KEY}"
        hash_code = hashlib.sha256(raw.encode()).hexdigest()[:12].upper()
        return f"{school_name[:4].upper()}-{year}{month:02d}-{hash_code}"

    @staticmethod
    def verify_code(school_name, code):
        """App uses this to check if code is valid"""
        try:
            parts = code.split("-")
            year_month = parts[1]
            year = int(year_month[:4])
            month = int(year_month[4:6])

            expected = Subscription.generate_code(school_name, year, month)
            return expected == code
        except:
            return False

    @staticmethod
    def save_license(code, expiry_date):
        with open(LICENSE_FILE, "w") as f:
            json.dump({"code": code, "expiry": expiry_date}, f)

    @staticmethod
    def load_license():
        if not os.path.exists(LICENSE_FILE):
            return None
        with open(LICENSE_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def check_status(school_name):
        lic = Subscription.load_license()
        if not lic:
            return False, "No License Found. Pay 2000 UGX to activate"

        now = datetime.now()
        expiry = datetime.strptime(lic["expiry"], "%Y-%m-%d")

        if now > expiry:
            return False, f"License Expired on {lic['expiry']}. Pay 2000 UGX to renew"

        if not Subscription.verify_code(school_name, lic["code"]):
            return False, "Invalid License Code. App Locked"

        days_left = (expiry - now).days
        return True, f"Active. Expires: {lic['expiry']} - {days_left} days left"
