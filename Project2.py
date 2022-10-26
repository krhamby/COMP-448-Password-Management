import hashlib as hash
import base64 as encoder
import os
import secrets

# Use the following technique to store password
# Base64 ( SHA-512 ( password || Base64( salt )))

# Command line
if __name__ == '__main__':
    while True:
        print("Please use one of the following commands:")
        print("> add-user <username> <password>")
        print("> check-password <username> <password>")
        print("> remove-user <username>")
        print("> print")
        print("> end")
        
        command = input("Enter command: ").split()
        
        # add-user <username> <password>
        if command[0] == "add-user":
            username = command[1]
            password = command[2]
            
            # generate salt and encode with Base64
            ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            salt = ''.join(secrets.choice(ALPHABET) for i in range(16))
            salt = encoder.b64encode(salt.encode('utf-8'))
            
            # hash and encode password + salt
            passHash = encoder.b64encode(hash.sha512((password + salt.decode('utf-8')).encode()).digest())
            
            # store in file
            with open("Project2PW.txt", 'a') as file:
                file.write(username + ":$6$" + salt.decode('utf-8') + "$" + passHash.decode('utf-8') + "\n")
        
        # check-password <username> <password>
        elif command[0] == "check-password":
            username = command[1]
            password = command[2]
            
            # get salt and hash from file
            salt = ""
            passHash = ""
            while True:
                with open("Project2PW.txt", "r") as file:
                    for line in file:
                        if line.startswith(username):
                            salt = line.split("$")[2]
                            passHash = line.split("$")[3]
                            break
                    break
                
            # remove newline character
            passHash = passHash.strip()
            
            # encode passHash from string to bytes
            passHash.encode('utf-8')
            
            # compare with stored hash
            if passHash == encoder.b64encode(hash.sha512((password + salt).encode()).digest()).decode('utf-8'):
                print("Password is correct\n")
            else:
                print("Password is incorrect\n")
        
        # remove-user <username>
        elif command[0] == "remove-user":
            username = command[1]

            # remove line from file
            while True:
                with open("Project2PW.txt", "r") as file:
                    lines = file.readlines()
                with open("Project2PW.txt", "w") as file:
                    for line in lines:
                        if line.startswith(username):
                            continue
                        file.write(line)
                break
        
        # print
        elif command[0] == "print":
            with open("Project2PW.txt", "r") as file:
                print(file.read())
                
        # end
        elif command[0] == "end":
            break
        
        else:
            print("Invalid command\n")
            continue
        
        