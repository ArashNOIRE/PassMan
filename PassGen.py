import random as r

# Password generator function
# Parameters: UserwantNumber, UserwantSymbols, UserwantUpper, UserwantLower, UserLength
# Returns: Generated password string or None if invalid input
def main(UserwantNumber, UserwantSymbols, UserwantUpper,UserwantLower,UserLength):
    # Define character sets for password generation
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

    # Validate user input for numbers
    try:
        Fnum = UserwantNumber
        if Fnum not in ("y", "n"):
            print ("All you had to do was enter a damn valid input, USER!")
            return None
    except ValueError:
        print("Please enter a valid input.")
        return None

    # Validate user input for symbols
    try:
        Fsym = UserwantSymbols
        if Fsym not in ("y", "n"):
            print ("All you had to do was enter a damn valid input, USER!")
            return None
    except ValueError:
        print("Please enter a valid input.")
        return None

    # Validate user input for uppercase letters
    try:
        Fupr = UserwantUpper
        if Fupr not in ("y", "n"):
            print ("All you had to do was enter a damn valid input, USER!")
            return None
    except ValueError:
        print("Please enter a valid input.")
        return None

    # Validate user input for lowercase letters
    try:
        Flow = UserwantLower
        if Flow not in ("y", "n"):
            print ("All you had to do was enter a damn valid input, USER!")
            return None
    except ValueError:
        print("Please enter a valid input.")
        return None
    
    # Validate user input for password length
    try:
        Flen = UserLength
        if Flen <= 0:
            print ("All you had to do was enter a damn valid input, USER!")
            return None
    except ValueError:
        print("Please enter a valid input.")
        return None

    # Build the character pool based on user preferences
    final_base = []
    if Fupr == "y":
        final_base += upper_letters
    if Fnum == "y":
        final_base += numbers
    if Fsym == "y":
        final_base += symbols
    if Flow == "y":
       final_base += lower_letters
    
    # Generate password if character pool is not empty
    if len(final_base) == 0:
        return None
    else:
        # Randomly select characters from the pool
        for i in range(Flen):
            password += r.choice(final_base)
        return password

