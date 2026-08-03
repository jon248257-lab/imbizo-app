import json, os, hashlib

USER_FILE = "users.json"

def _hash(pw):
    """Simple hash so we don't store plain passwords"""
    return hashlib.sha256(pw.encode()).hexdigest()

def first_run():
    """Check if this is first time opening app"""
    return not os.path.exists(USER_FILE)

def create_admin(username, password, role="headteacher"):
    """First user. Always headteacher"""
    data = [{
        "username": username, 
        "password": _hash(password), 
        "role": role,
        "created": "admin"
    }]
    with open(USER_FILE, "w") as f:
        json.dump(data, f)
    return True

def add_user(username, password, role="teacher", created_by="headteacher"):
    """Headteacher can add new teachers"""
    users = load_users()
    if any(u["username"] == username for u in users):
        return False, "Username already exists"
    
    users.append({
        "username": username,
        "password": _hash(password),
        "role": role,
        "created": created_by
    })
    with open(USER_FILE, "w") as f:
        json.dump(users, f)
    return True, "User Created"

def login(username, password):
    """Return full user dict if login success, else None"""
    if not os.path.exists(USER_FILE): 
        return None
    
    users = load_users()
    hashed = _hash(password)
    
    for u in users:
        if u["username"] == username and u["password"] == hashed:
            return u # returns {"username":, "role":, "created":}
    
    return None

def load_users():
    """Load all users"""
    if not os.path.exists(USER_FILE): 
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)

def delete_user(username):
    """Headteacher can delete teachers"""
    users = load_users()
    users = [u for u in users if u["username"] != username]
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def get_role(username):
    users = load_users()
    for u in users:
        if u["username"] == username:
            return u["role"]
    return "teacher"
