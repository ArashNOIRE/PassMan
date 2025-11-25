import random as r
def main(Unum, Usym, Uupr,Ulow,Ulen):
    # Options for the password (dictionery)
    lower_letters = ["a","b","c","d","e","f","g","h","i","j",
                    "k","l","m","n","o","p","q","r","s","t",
                    "u","v","w","x","y","z"]
    upper_letters = ["A","B","C","D","E","F","G","H","I","J",
                     "K","L","M","N","O","P","Q","R","S","T",
                     "U","V","W","X","Y","Z"]
    numbers = ["1","2","3","4","5","6","7","8","9","0"]
    symbols = ["@", "-", "_", "|", "~", "/", ".", ",", "#", "$",
                "%", "&", "*", "+", "!", "?", "^", "=", "{", "}",
                "[", "]", "(", ")","`", ";", ":", "<", ">", "\\"]
    password = ""

    # Options to choose
    try:
        Cnum = Unum
        if Cnum != "y" or "n":
            print ("All you had to do was enter a damn valid input, USER!")
            exit()
    except ValueError:
        print("Please enter a valid input.")

    try:
        Csym = Usym
        if Csym != "y" or "n":
            print ("All you had to do was enter a damn valid input, USER!")
            exit()
    except ValueError:
        print("Please enter a valid input.")

    try:
        Cupr = Uupr
        if Cupr != "y" or "n":
            print ("All you had to do was enter a damn valid input, USER!")
            exit()
    except ValueError:
        print("Please enter a valid input.")

    try:
        Clow = Ulow
        if Clow != "y" or "n":
            print ("All you had to do was enter a damn valid input, USER!")
            exit()
    except ValueError:
        print("Please enter a valid input.")
    
    try:
        Clen = Ulen
        if Clen <= 0:
            print ("All you had to do was enter a damn valid input, USER!")
            exit()
    except ValueError:
        print("Please enter a valid input.")

    final_base = []
    ## User choose what he/she wants
    if Cupr == "y":
        final_base += upper_letters
    if Cnum == "y":
            final_base += numbers
    if Csym == "y":
        final_base += symbols
    if Clow == "y":
       final_base += lower_letters
    ### check if the inputs are valid
    if len(final_base) == 0:
        print("All you had to do was enter a damn valid input, USER!")
    else:
        for i in range(Clen):
            password += r.choice(final_base)
        print("Your password is:", password)

print ("Welcome to my 2000's password generator!")
# Todo:
#   Rename Vars
#   Make it like an API
