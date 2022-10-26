# Authors: Kevin Hamby, Melva Loock, Philippe Keita
# Course: COMP 448
# Assignment: Project 2
# Date: 10/25/2023

import hashlib as hash
import base64 as encoder
import os
import secrets

def is_username_available(username):
    # Check if username is present in the file
    with open("Project2PW.txt", "r") as file:
        for line in file:
            if line.startswith(username):
                return False
    return True

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
        if len(command) == 3 and command[0] == "add-user":
            username = command[1]
            password = command[2]
            
            # make sure username and password are in ascii
            if not username.isascii or not password.isascii:
                print("\u001b[31mUsername and password must use ASCII characters\u001b[0m\n")
                continue
            # make sure the username is not already taken
            elif not is_username_available(username):
                print("\u001b[31mUsername is not available\u001b[0m\n")
                continue
            else:     
                # generate salt and encode with Base64
                ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                salt = ''.join(secrets.choice(ALPHABET) for i in range(16))
                salt = encoder.b64encode(salt.encode('ascii'))
                
                # hash and encode password + salt
                passHash = encoder.b64encode(hash.sha512((password + salt.decode('ascii')).encode()).digest())
                
                # store in file
                with open("Project2PW.txt", 'a') as file:
                    file.write(username + ":$6$" + salt.decode('ascii') + "$" + passHash.decode('ascii') + "\n")
                    
                # confirm
                if not is_username_available(username):
                    print("\u001b[32mUser added\u001b[0m\n")
            
        # check-password <username> <password>
        elif len(command) == 3 and command[0] == "check-password":
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
            passHash.encode('ascii')
            
            # compare with stored hash
            if passHash == encoder.b64encode(hash.sha512((password + salt).encode()).digest()).decode('ascii'):
                print("\u001b[32mPassword is correct\u001b[0m \n")
            else:
                print("\u001b[31mPassword is incorrect\u001b[0m \n")
        
        # remove-user <username>
        elif len(command) ==2 and command[0] == "remove-user":
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
            
            # Check that the user is not present in the file
            if is_username_available(username):
                print("\u001b[32mUser removed or does not exist\u001b[0m\n")
        
        # print the whole file as is
        elif len(command) == 1 and command[0] == "print":
            with open("Project2PW.txt", "r") as file:
                print(file.read())
                
        # end the while loop
        elif len(command) == 1 and command[0] == "end":
            break
        
        # catch misc. invalid commands
        else:
            print("\u001b[31mInvalid command\u001b[0m\n")
            continue
        
        