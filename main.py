import PassGen
import Pass2File

Passwords={}

NewPassword=PassGen.main("y","y","y","y",16)
Passgogol = "Google.com"
Passwords[Passgogol] = NewPassword
Pass2File.save_passwords(Passwords)

LoadedPasswords = Pass2File.load_passwords()
print("Loaded Passwords:", LoadedPasswords)# save to file
