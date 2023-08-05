import hashlib
import os
import random
import string

class Password:

    def __init__(self):
        self.name = "Google"
        self.url = "Sample"
        self.username = "John_Doe"
        self.password_loc = f"/passwords/{self.name}.passfile"
        self.password = "password"


passwords = []
user_details = ""


def password_check(username, password):
    salt = random.choices(string.ascii_letters, k=5)
    if os.path.isfile("pass.hash"):
        global user_details
        pass_user = username + password
        pass_user_hash = hashlib.sha256(bytes(pass_user + salt, "utf-8"))
        user_details = pass_user

        with open("pass.hash", "r") as f:
            file_pass = f.readline()
            f.close()

        if pass_user_hash.hexdigest() == file_pass:
            return "Access granted!"
        else:
            return "Fuck off! Access denied!"
    else:
        save_login_details(password=password, username=username)


def save_login_details(username, password):
    with open('pass.hash', "w") as f:
        pass_text = username + password
        pass_hash = hashlib.sha256(bytes(pass_text, "utf-8"))
        f.write(pass_hash.hexdigest())
        f.close()
