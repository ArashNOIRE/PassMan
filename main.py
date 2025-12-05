import PassGen
import Pass2File
from Pass2File import hash_password, verify_integrity, MASTER_FILE


# Setup master password on first run
def setup_master():
    import os
    if os.path.exists(MASTER_FILE):
        return

    pwd = input("Set a master password: ")
    pwd2 = input("Confirm master password: ")

    if pwd != pwd2:
        print("Passwords do not match. Exiting.")
        exit()

    master_hash = hash_password(pwd)
    
    # Create master.key with master password hash and placeholder hashes
    with open(MASTER_FILE, "w") as f:
        f.write(master_hash + "\n")
        f.write("none\n")
        f.write("none")

    print("Master password created!")

# Verify master password on each run
def verify_master():
    import os
    if not os.path.exists(MASTER_FILE):
        print("Master password file missing!")
        exit()

    with open(MASTER_FILE, "r") as f:
        lines = f.read().splitlines()
    saved_hash = lines[0]

    # Allow 3 attempts to enter correct master password
    for attempt in range(3):
        pwd = input("Enter master password: ")
        if hash_password(pwd) == saved_hash:
            print("Access granted.")
            return True
        else:
            print("Wrong password.")

    print("Too many attempts. Exiting.")
    exit()

# --- Password Management Functions ---

# Global dictionary to store passwords
Passwords = {}

# Add a new password for a website
def add_password(website, password):
    Passwords[website] = password
    Pass2File.save_passwords(Passwords)
    print(f"Password: {password} for {website} added.")

# Display all stored passwords
def see_password():
    sure = input("Are you sure you want to see all passwords? (y/n): ")
    if sure.lower() == "y":
        for site, pwd in Passwords.items():
            print(f"{site}: {pwd}")
    else:
        print("Cancelled.")

# Remove a password for a website
def remove_password(website):
    if website in Passwords:
        del Passwords[website]
        Pass2File.save_passwords(Passwords)
        print(f"Password for {website} removed.")
    else:
        print("Website not found.")

# Rename a website entry
def rename_website(old_website, new_website):
    if old_website in Passwords:
        Passwords[new_website] = Passwords.pop(old_website)
        Pass2File.save_passwords(Passwords)
        print(f"Website renamed from {old_website} to {new_website}.")
    else:
        print("Old website not found.")

# Update the password for a website
def change_password(website, new_password):
    if website in Passwords:
        Passwords[website] = new_password
        Pass2File.save_passwords(Passwords)
        print(f"Password for {website} updated.")
    else:
        print("Website not found.")

# Search and display password for a specific website
def search_password(website):
    if website in Passwords:
        print(f"Password for {website}: {Passwords[website]}")
    else:
        print("Website not found.")

# Main menu and command handler
def main():
    global Passwords
    what = input("What do you want to do? \n(add, remove, see, rename, change, search, exit): ")
    verify_integrity()
    Passwords = Pass2File.load_passwords()

    if what == "add":
        # Option to generate password or enter manually
        website = input("Enter website: ")
        gen_choice = input("Generate password? (y/n): ")
        if gen_choice.lower() == "y":
            num = input("Include numbers? (y/n): ")
            sym = input("Include symbols? (y/n): ")
            upr = input("Include uppercase letters? (y/n): ")
            low = input("Include lowercase letters? (y/n): ")
            length = int(input("Enter password length: "))
            password = PassGen.main(num, sym, upr, low, length)
        else:
            password = input("Enter password: ")
        add_password(website, password)
    elif what == "remove":
        remove_password(input("Enter website to remove: "))
    elif what == "see":
        see_password()
    elif what == "rename":
        rename_website(input("Enter old website name: "), input("Enter new website name: "))
    elif what == "change":
        change_password(input("Enter website to change password: "), input("Enter new password: "))
    elif what == "search":
        search_password(input("Enter website to search: "))
    elif what == "exit":
        print("Exiting Password Manager.")
        exit()
    elif what == "clear":
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("Invalid option.")

# Entry point - initialize master password and start main loop
if __name__ == "__main__":
    setup_master()
    verify_master()

    print("Welcome to the Password Manager!")
    while True:
        main()
