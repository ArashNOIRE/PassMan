import PassGen
import Pass2File

# Initialize an empty dictionary to store passwords BTW: Not safe!
Passwords={}
### Test example of generating and saving a password
#    NewPassword=PassGen.main("y","y","y","y",16)
#   Passgogol = "Google.com"
#   Passwords[Passgogol] = NewPassword
#   Pass2File.save_passwords(Passwords)
#
#   Passwords = Pass2File.load_passwords()
#   print("Loaded Passwords:", Passwords)# save to file
###
def add_password(website, password):
    Passwords[website] = password
    Pass2File.save_passwords(Passwords)
    print(f"Password: {password} for {website} added.")

def see_password():
    sure=input("Are you sure you want to see all passwords? (y/n): ")
    if sure.lower() == "y":
            for site, pwd in Passwords.items():
                print(f"{site}: {pwd}")
    else:    
        print("Cancelled.")
        return




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
    Passwords = Pass2File.load_passwords()


    if what == "add":
        add_password(input("Enter website: "), input("Enter password (or type 'gen' to generate one): ") if input("Generate password? (y/n): ") == "n" else PassGen.main(input("Include numbers? (y/n): "), input("Include symbols? (y/n): "), input("Include uppercase letters? (y/n): "), input("Include lowercase letters? (y/n): "), int(input("Enter password length: "))))
    
    elif what == "remove":
        remove_password(input("Enter website to remove: ")) 
    
    elif what == "see":
        see_password()
    
    elif what == "rename":
        rename_website(input("Enter old website name: "), input("Enter new website name: "))
    
    elif what == "change":
        change_password(input("Enter website to change password: "), input("Enter new password: "))
    
    elif what == "exit":
        print("Exiting Password Manager.")
        exit()
        return
    
    elif what == "search":
        search_password(input("Enter website to search: "))
    
    elif what == "clear":
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    else:
        print("Invalid option.")



if __name__ == "__main__":
    print("Welcome to the Password Manager!")
    while True:
        main()