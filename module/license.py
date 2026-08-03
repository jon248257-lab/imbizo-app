import os, json, hashlib, datetime, secrets, string, uuid

LICENSE_FILE = "data/license.kr"

# CHANGE THIS BEFORE YOU COMPILE AND RELEASE. MUST MATCH GENERATOR.PY
SECRET = "DR_SCHOOL_2026!CEO_JON#K9p@LzQ7$xWvR"

PRICES = {
    "teacher": {"month": 2000, "term": 5000},
    "headteacher": {"month": 3000, "term": 7500}
} # FIXED: Added closing }

DAYS = {"month": 30, "term": 90} # DSTV style stacking

def get_device_id():
    """Lock license to this phone using MAC address. More secure"""
    mac = uuid.getnode()
    return hashlib.sha256(str(mac).encode()).hexdigest()

def _make_signature(base_code, device_id, admin_phone, expiry_str, role, plan):
    """Internal: Creates tamper-proof signature"""
    raw = f"{base_code}{device_id}{admin_phone}{expiry_str}{role}{plan}{SECRET}"
    return hashlib.sha256(raw.encode()).hexdigest()

def generate_base_code(role="teacher", plan="month"):
    """Admin uses this to generate codes to sell. For your PC only"""
    chars = string.ascii_uppercase + string.digits
    base_code = '-'.join([''.join(secrets.choice(chars) for _ in range(4)) for _ in range(3)])
    expiry = datetime.datetime.now() + datetime.timedelta(days=DAYS[plan])
    return base_code, expiry.strftime("%Y-%m-%d"), role, plan

def create_full_license(base_code, admin_phone, role, plan):
    """This is called when user enters code in app"""
    device_id = get_device_id()

    # 1. CHECK FOR EXISTING LICENSE - DSTV STACKING
    current_expiry_dt = datetime.datetime.now()
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            try:
                old_data = json.load(f)
                # Only stack if same device AND same role
                if old_data["device_id"] == device_id and old_data["role"] == role:
                    old_expiry = datetime.datetime.strptime(old_data["expiry"], "%Y-%m-%d")
                    if old_expiry > current_expiry_dt: # if still active, stack on top
                        current_expiry_dt = old_expiry
            except: pass

    # 2. ADD NEW DAYS ON TOP
    new_expiry_dt = current_expiry_dt + datetime.timedelta(days=DAYS[plan])
    new_expiry_str = new_expiry_dt.strftime("%Y-%m-%d")

    # 3. CREATE SIGNATURE TO PREVENT TAMPERING
    signature = _make_signature(base_code, device_id, admin_phone, new_expiry_str, role, plan)

    data = {
        "base_code": base_code,
        "device_id": device_id,
        "admin_phone": admin_phone,
        "expiry": new_expiry_str,
        "role": role,
        "plan": plan,
        "signature": signature
    }

    os.makedirs("data", exist_ok=True)
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return True, f"Active until {new_expiry_str}"

def check_license():
    """Returns: active, days_left, message"""
    if not os.path.exists(LICENSE_FILE):
        return False, 0, "No Activation Code found"

    try:
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
    except:
        return False, 0, "Corrupted License File"

    # 1. CHECK DEVICE LOCK FIRST
    if data["device_id"]!= get_device_id():
        return False, 0, "REJECTED: This code is locked to another phone"

    # 2. CHECK SIGNATURE - Prevents editing expiry
    check_sig = _make_signature(data['base_code'], data['device_id'], data['admin_phone'], data['expiry'], data['role'], data['plan'])
    if check_sig!= data["signature"]:
        return False, 0, "REJECTED: License tampered"

    # 3. CHECK EXPIRY + GRACE PERIOD
    expiry = datetime.datetime.strptime(data["expiry"], "%Y-%m-%d")
    days_left = (expiry - datetime.datetime.now()).days

    if days_left < 0:
        if days_left >= -3: # 3 day grace period
            return True, days_left, f"Grace Period. Expired {abs(days_left)} days ago"
        else:
            return False, 0, f"Activation expired on {data['expiry']}. Please renew."

    return True, days_left, f"{data['role'].title()} Active - {days_left} days left"

def get_renewal_alert(days_left):
    """Auto alerts at 7, 4, 1 days"""
    if days_left == 7: return "Reminder: Activation expires in 7 days."
    if days_left == 4: return "Urgent: Activation expires in 4 days."
    if days_left == 1: return "Final: Activation expires TOMORROW."
    return None

def get_current_role():
    if not os.path.exists(LICENSE_FILE): return "teacher"
    with open(LICENSE_FILE) as f: data = json.load(f)
    return data.get("role", "teacher")
