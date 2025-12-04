import PassGen
import Pass2File
from Pass2File import hash_password, verify_integrity

MASTER_FILE = "master.key"

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
    
    with open(MASTER_FILE, "w") as f:
        f.write(master_hash + "\n")
        f.write("none\n")
        f.write("none")

    print("Master password created!")

def verify_master():
    import os
    if not os.path.exists(MASTER_FILE):
        print("Master password file missing!")
        exit()

    with open(MASTER_FILE, "r") as f:
        lines = f.read().splitlines()
    saved_hash = lines[0]

    for attempt in range(3):
        pwd = input("Enter master password: ")
        if hash_password(pwd) == saved_hash:
            print("Access granted.")
            return True
        else:
            print("Wrong password.")

    print("Too many attempts. Exiting.")
    exit()

# --- dictionary ---
Passwords = {}

def add_password(website, password):
    Passwords[website] = password
    Pass2File.save_passwords(Passwords)
    print(f"Password: {password} for {website} added.")

def see_password():
    sure = input("Are you sure you want to see all passwords? (y/n): ")
    if sure.lower() == "y":
        for site, pwd in Passwords.items():
            print(f"{site}: {pwd}")
    else:
        print("Cancelled.")

def remove_password(website):
    if website in Passwords:
        del Passwords[website]
        Pass2File.save_passwords(Passwords)
        print(f"Password for {website} removed.")
    else:
        print("Website not found.")

def rename_website(old_website, new_website):
    if old_website in Passwords:
        Passwords[new_website] = Passwords.pop(old_website)
        Pass2File.save_passwords(Passwords)
        print(f"Website renamed from {old_website} to {new_website}.")
    else:
        print("Old website not found.")

def change_password(website, new_password):
    if website in Passwords:
        Passwords[website] = new_password
        Pass2File.save_passwords(Passwords)
        print(f"Password for {website} updated.")
    else:
        print("Website not found.")

def search_password(website):
    if website in Passwords:
        print(f"Password for {website}: {Passwords[website]}")
    else:
        print("Website not found.")

def main():
    global Passwords
    what = input("What do you want to do? \n(add, remove, see, rename, change, search, exit): ")
    verify_integrity()
    Passwords = Pass2File.load_passwords()

    if what == "add":
        add_password(
            input("Enter website: "),
            input("Enter password (or type 'gen' to generate one): ")
            if input("Generate password? (y/n): ") == "n"
            else PassGen.main(
                input("Include numbers? (y/n): "),
                input("Include symbols? (y/n): "),
                input("Include uppercase letters? (y/n): "),
                input("Include lowercase letters? (y/n): "),
                int(input("Enter password length: "))
            )
        )
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

if __name__ == "__main__":
    setup_master()
    verify_master()

    print("Welcome to the Password Manager!")
    while True:
        main()
