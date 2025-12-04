from cryptography.fernet import Fernet
import json
import os

KEY_FILE = "key.key"
PASS_FILE = "passwords.enc"

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

key = load_key()
cipher = Fernet(key)

def save_passwords(passwords):
    data = json.dumps(passwords).encode()
    encrypted = cipher.encrypt(data)
    with open(PASS_FILE, "wb") as f:
        f.write(encrypted)

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