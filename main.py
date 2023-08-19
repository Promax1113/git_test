import requests
from datetime import timedelta, datetime

import json
import os
import shutil
import sys
import textwrap
import time
from getpass import getpass


import password_access
import password_generator
import password_processing


def user_menu():
    menu = "a"
    try:
        menu = int(input(textwrap.fill(
            "Press 1 for saving a password, 2 for reading a password, 3 to generate one, 4 to delete one or 5 to quit: ",
            width=shutil.get_terminal_size().columns)))
    except:

        print("\nBad choice, try again!\n")
        user_menu()

    if menu == 1:
        user_save_password()
    elif menu == 2:
        user_read_password()
    elif menu == 3:
        user_generate_password()
    elif menu == 4:
        user_delete_password()
    elif menu == "yes":
        # TODO: Add Multi users!!
        user_settings()
    elif menu == 5:
        sys.exit()
    else:
        print("\nInvalid option!\n")
        user_menu()


def user_generate_password():
    generated = password_generator.generate_password()
    print(f"Here's your 20 character random password: {generated}")
    choice = input("Would you like to save it as a new password? (y/n): ").lower()
    if choice == "y":
        save_generated_password(generated)
        user_menu()
    else:
        user_menu()


def save_generated_password(__password):
    print("Now you're gonna need to input some login details for the website.")
    if input("1 to continue, 2 to go back: ") == "1":
        name = input("Name of the password file (not the password): ").lower()
        if name == __password:
            print("\nInvalid Password name, cannot be the same as password.\n")
            save_generated_password(__password)
        website = input("Website where the password is used: ")
        email = input("Would you like a temporal email? (y/n): ").lower()
        if email == "y":
            generate_email(name, website, __password)
        else:
            _username = input("Username used with the password: ")
            password_access.save_password(name, website, _username, __password)
            print("Password saved successfully!")

    else:
        user_menu()


def user_save_password():
    print("Now you're gonna need to input some login details for the website.")
    if input("1 to continue, 2 to go back: ") == "1":

        name = input("Name of the password file (not the password): ").lower()
        website = input("Website where the password is used: ")
        _username = input("Username used with the password: ")
        _password = getpass("Password used with the username: ")
        if _password in name and _password == name:
            print("\nInvalid Password name, cannot be the same as password.\n")
            print("\nPassword was NOT saved!!\n")

            user_save_password()
        password_access.save_password(name, website, _username, _password)
        print("Password saved successfully!")
        user_menu()
    else:
        user_menu()


def user_read_password():
    print("\nCurrently saved passwords: ")
    index = 0
    if not os.listdir(f"{password_access.userpath}/passwords/"):
        print("There aren't any saved passwords. Returning to menu!\n")
        time.sleep(1.5)
        user_menu()
    for file in os.listdir(f"{password_access.userpath}/passwords/"):

        if file.endswith(".passfile"):
            index += 1
            name = file.split('.')
            print(f"{index}. {name[0]}")
    choice = input("Name of the password (Ensure it's the same as shown!): ").lower()
    choice_pass = password_access.read_password(choice)
    if choice_pass == "File not found!":
        print("\nFile not found!\n")
    else:
        print("Password details:")
        print(
              f"\nName: {choice_pass['name']},"
              f" Website: {choice_pass['website']},"
              f" Username: {choice_pass['username']},"
              f" Password: {choice_pass['password']}\n"
              )
    user_menu()

# deprecated
def user_settings():
    global username
    global password
    print(f"Current login details: \nUsername: {username}, Password: {password}")
    if input("Would you like to change them? (y/n): ").lower() == "y":
        _username = input("New username: ")
        _password = input("New password: ")
        print("Confirm them.")
        username_c = input("New username again: ")
        password_c = input("New password again: ")
        if password_c == _password and username_c == _username:
            password = password_c
            username = username_c
            password_processing.save_login_details(username, password)
            print(f"Your new login details are: ")
            print(f"Username: {username}")
            print(f"Password: {password}")
            user_menu()
        else:
            print("Passwords do not match!")
            user_settings()
    else:
        user_menu()


def user_delete_password():
    print("\nCurrently saved passwords: ")
    index = 0
    if not os.listdir(f"{password_access.userpath}/passwords/"):
        print("There aren't any saved passwords. Returning to menu!\n")
        time.sleep(1.5)
        user_menu()
    for file in os.listdir(f"{password_access.userpath}/passwords/"):
        if file.endswith(".passfile"):
            index += 1
            name = file.split('.')
            print(f"{index}. {name[0]}")
    choice = input("Name of the password (Ensure it's the same as shown!): ").lower()
    if f"{choice}.passfile" not in os.listdir(f"{password_access.userpath}/passwords/"):
        print("\nFile not found!\n")
        user_menu()
    else:
        if input(f"Are you sure you want to delete {choice}? (y/n): ").lower() == "y":
            os.remove(f"{password_access.userpath}/passwords/{choice}.passfile")
            os.remove(f"{password_access.userpath}/passwords/{choice}.data")
            print(f"{choice} removed successfully!")
            user_menu()
        else:
            print("\nNothing was deleted!\n")
            time.sleep(1)
            user_menu()



def generate_email(_name, _website, _password):
    old = True

    prefix = "https://www.1secmail.com/api/v1/"
    get_message = "?action=getMessages"
    read_message = "?action=readMessage"
    email = "?action=genRandomMailbox&count=1"
    email_address_json = json.loads(requests.get(f"{prefix}{email}").text)
    email_address = email_address_json[0]
    email_address = email_address.split("@")
    login, domain = email_address[0], email_address[1]
    print(f"Your email is: {email_address_json[0]}")
    print(textwrap.fill(
        "You will now be able to read any message that enters this temporal inbox. It will update every 5 seconds.",
        width=shutil.get_terminal_size().columns))
    data = []
    email_ids = []
    if input("Are you waiting for a code? (y/n): ").lower() == "y":
        while old:
            data = json.loads(requests.get(f"{prefix}{get_message}&login={login}&domain={domain}").text)
            if data:
                email_time = datetime.strptime(data[0]['date'], "%Y-%m-%d %H:%M:%S")
                time.sleep(5)
                print(f"Last email sent to this address was from {email_time} and from {data[0]['from']}: ")

                if email_time > (datetime.now().replace(microsecond=0)) - timedelta(minutes=10):
                    old = False

            else:
                time.sleep(5)
                print("No E-Mails received!")

    else:
        print("Saving password data...")
        password_access.save_password(_name, _website, f"{login}@{domain}", _password)
        time.sleep(1)
        print("Saved!")
        user_menu()

    for item in data:
        email_ids.append(item["id"])
    for email_id in email_ids:
        email = requests.get(f"{prefix}{read_message}&login={login}&domain={domain}&id={email_id}")

        verif = json.loads(email.text)
        print(f"Code: {verif['textBody']}")
        time.sleep(10)
    password_access.save_password(_name, _website, f"{login}@{domain}", _password)
    time.sleep(2.5)
    print("Password saved with that email!")


if __name__ == "__main__":

    if not os.path.isfile("pass.hash"):
        try:
            os.mkdir(f"{password_access.userpath}/passwords/")
        finally:
            pass

        print(
            "Enter your username and password. You will need to remember these to see your other passwords saved or you won't be able to!")

    result = ""
    while not result == "Access granted!" or result is None:
        username = input("Username: ")
        while " " in username:
            print("Username cannot contain spaces!")
            username = input("Username: ")
        password = getpass()
        result = password_processing.password_check(username, password)

        if result is None:
            print("Saved your Password!")
            user_menu()
        else:
            print(result)
    user_menu()
