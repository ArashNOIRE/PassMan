from cryptography.fernet import Fernet
import json
import os
import hashlib

# File paths for encryption key, encrypted passwords, and master password
KEY_FILE = "key.key"
PASS_FILE = "passwords.enc"
MASTER_FILE = "master.key"

# --- Helper Functions ---

# Hash a password using SHA-256
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

# Calculate SHA-256 hash of a file
def file_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# --- Encryption Key Management ---

# Load or generate encryption key for Fernet cipher
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

# --- File Integrity Verification ---

# Verify the integrity of key.key and passwords.enc using hashes stored in master.key
def verify_integrity():
    if not os.path.exists(MASTER_FILE):
        print("Error: master.key missing!")
        exit()

    with open(MASTER_FILE, "r") as f:
        lines = f.read().splitlines()

    # Line 2: Hash of key.key
    expected_key_hash = lines[1] if len(lines) > 1 and lines[1] != "none" else None
    if expected_key_hash and expected_key_hash != file_hash(KEY_FILE):
        print("Error: key.key modified or invalid!")
        exit()

    # Line 3: Hash of passwords.enc
    expected_pass_hash = lines[2] if len(lines) > 2 and lines[2] != "none" else None
    if expected_pass_hash and os.path.exists(PASS_FILE):
        if expected_pass_hash != file_hash(PASS_FILE):
            print("Error: passwords.enc modified or corrupted!")
            exit()

# Update the hashes in master.key after saving passwords
def update_master_hashes():
    """Updates the actual hashes of key.key and passwords.enc in master.key"""
    if not os.path.exists(MASTER_FILE):
        return

    with open(MASTER_FILE, "r") as f:
        lines = f.read().splitlines()

    # Line 1: master password hash (preserve)
    master_hash = lines[0] if len(lines) > 0 else "none"
    # Line 2: hash of key.key
    key_hash = file_hash(KEY_FILE) or "none"
    # Line 3: hash of passwords.enc
    pass_hash = file_hash(PASS_FILE) or "none"

    with open(MASTER_FILE, "w") as f:
        f.write(master_hash + "\n")
        f.write(key_hash + "\n")
        f.write(pass_hash)

# --- Password Encryption/Decryption ---

# Encrypt and save passwords dictionary to file
def save_passwords(passwords):
    data = json.dumps(passwords).encode()
    encrypted = cipher.encrypt(data)
    with open(PASS_FILE, "wb") as f:
        f.write(encrypted)
    # Update integrity hashes after saving
    update_master_hashes()

# Load and decrypt passwords from file
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
