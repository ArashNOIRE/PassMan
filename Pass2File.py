from cryptography.fernet import Fernet
import json
import os
import hashlib

KEY_FILE = "key.key"
PASS_FILE = "passwords.enc"
MASTER_FILE = "master.key"

# --- کمکی‌ها ---
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def file_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# --- کلید ---
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read()
        if len(key) != 44:  # base64-encoded 32-byte key
            raise ValueError("Invalid Fernet key in key.key")
        return key
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

key = load_key()
cipher = Fernet(key)

# --- Integrity ---
def verify_integrity():
    if not os.path.exists(MASTER_FILE):
        print("Error: master.key missing!")
        exit()

    with open(MASTER_FILE, "r") as f:
        lines = f.read().splitlines()

    # خط دوم: hash کلید
    expected_key_hash = lines[1] if len(lines) > 1 and lines[1] != "none" else None
    if expected_key_hash and expected_key_hash != file_hash(KEY_FILE):
        print("Error: key.key modified or invalid!")
        exit()

    # خط سوم: hash پسوردها
    expected_pass_hash = lines[2] if len(lines) > 2 and lines[2] != "none" else None
    if expected_pass_hash and os.path.exists(PASS_FILE):
        if expected_pass_hash != file_hash(PASS_FILE):
            print("Error: passwords.enc modified or corrupted!")
            exit()

def update_master_hashes():
    """بعد از ساخت یا ذخیره پسوردها، hash واقعی key.key و passwords.enc را در master.key بروزرسانی می‌کند"""
    if not os.path.exists(MASTER_FILE):
        return

    with open(MASTER_FILE, "r") as f:
        lines = f.read().splitlines()

    # خط اول: master hash (حفظ شود)
    master_hash = lines[0] if len(lines) > 0 else "none"
    # خط دوم: hash key.key
    key_hash = file_hash(KEY_FILE) or "none"
    # خط سوم: hash passwords.enc
    pass_hash = file_hash(PASS_FILE) or "none"

    with open(MASTER_FILE, "w") as f:
        f.write(master_hash + "\n")
        f.write(key_hash + "\n")
        f.write(pass_hash)

# --- پسوردها ---
def save_passwords(passwords):
    data = json.dumps(passwords).encode()
    encrypted = cipher.encrypt(data)
    with open(PASS_FILE, "wb") as f:
        f.write(encrypted)
    update_master_hashes()

def load_passwords():
    if not os.path.exists(PASS_FILE):
        return {}

    with open(PASS_FILE, "rb") as f:
        encrypted = f.read()

    try:
        decrypted = cipher.decrypt(encrypted)
    except:
        print("Error: password file is corrupted or wrong key.")
        return {}

    return json.loads(decrypted.decode())
