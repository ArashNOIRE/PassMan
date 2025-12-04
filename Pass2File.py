import json
import os

# storage to file
PASSWORDS_FILE = "passes.json"

# if file exist read it, else make it
def load_passwords():
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as f:
            return json.load(f)
    return {}

# save to file
def save_passwords(passwords):
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(passwords, f)

#

