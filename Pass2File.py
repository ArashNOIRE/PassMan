from cryptography.fernet import Fernet
import json
import os
import hashlib

KEY_FILE = "key.key"
PASS_FILE = "passwords.enc"
MASTER_FILE = "master.key"

# Simple hashing function for passwords
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def file_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def update_key_hash():
    if os.path.exists(PASS_FILE):
        with open(KEY_FILE, "rb+") as f:
            lines = f.read().splitlines()
            key_data = lines[:-1] 
            new_hash = file_hash(PASS_FILE).encode()
            f.seek(0)
            f.truncate()
            for line in key_data:
                f.write(line + b"\n")
            f.write(new_hash)

def verify_integrity():
    if not os.path.exists(MASTER_FILE):
        print("Error: master.key missing!")
        exit()

    with open(MASTER_FILE, "r") as f:
        lines = f.read().splitlines()

    # بررسی خط دوم master.key
    expected_key_hash = lines[1] if len(lines) > 1 else None
    if expected_key_hash and expected_key_hash != file_hash(KEY_FILE):
        print("Error: key.key modified or invalid!")
        exit()

    # بررسی key.key → passwords.enc
    if os.path.exists(KEY_FILE) and os.path.exists(PASS_FILE):
        with open(KEY_FILE, "rb") as f:
            key_lines = f.read().splitlines()
        if key_lines[-1].decode() != file_hash(PASS_FILE):
            print("Error: passwords.enc modified or corrupted!")
            exit()


def load_key():
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, "rb").read()
    else:
        # ساخت کلید جدید
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

        # وابستگی با passwords.enc: ذخیره hash فایل پسورد در آخر key.key
        if os.path.exists(PASS_FILE):
            with open(KEY_FILE, "ab") as f:
                f.write(b"\n" + file_hash(PASS_FILE).encode())

    return key
key = load_key()
cipher = Fernet(key)

def save_passwords(passwords):
    data = json.dumps(passwords).encode()
    encrypted = cipher.encrypt(data)
    with open(PASS_FILE, "wb") as f:
        f.write(encrypted)
    update_key_hash()

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