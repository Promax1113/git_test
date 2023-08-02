import password_processing
import password_access
import password_generator
import os
from getpass import getpass
import requests
import json
import time
from datetime import timedelta, timezone, datetime


def user_menu():
    menu = int(input("Press 1 for saving a password, 2 for reading a password, 3 to generate one, 4 to delete one or 6 to quit: "))

    if menu == 1:
        user_save_password()
    elif menu == 2:
        user_read_password()
    elif menu == 3:
        user_generate_password()
    elif menu == 4:
        user_delete_password()
    elif menu == "yes":
        # TODO Add Multi users!!
        user_settings()
    elif menu == 5:
        exit(0)
    else:
        exit(0)


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
        name = input("Name of the password: ")
        website = input("Website where the password is used: ")
        _username = input("Username used with the password: ")
        password_access.save_password(name, website, _username, __password)
        print("Password saved successfully!")

    else:
        user_menu()


def user_save_password():
    print("Now you're gonna need to input some login details for the website.")
    if input("1 to continue, 2 to go back: ") == "1":

        name = input("Name of the password: ").capitalize()
        website = input("Website where the password is used: ")
        _username = input("Username used with the password: ")
        _password = getpass("Password used with the username: ")
        password_access.save_password(name, website, _username, _password)
        print("Password saved successfully!")
        user_menu()
    else:
        user_menu()


def user_read_password():
    print("Currently saved passwords: ")
    index = 0
    for file in os.listdir(f"{password_access.userpath}/passwords/"):
        if os.listdir(f"{password_access.userpath}/passwords/") == []:
            print("There aren't any saved passwords. Returning to menu!")
            user_menu()
        if file.endswith(".passfile"):
            index += 1
            name = file.split('.')
            print(f"{index}. {name[0]}")
    choice = input("Name of the password (Ensure it's the same as shown!): ")
    choice_pass = password_access.read_password(choice)
    print("Password details:")
    print(
        f"Name: {choice_pass['name']},"
        f" Website: {choice_pass['website']},"
        f" Username: {choice_pass['username']},"
        f" Password: {choice_pass['password']}"
    )
    user_menu()


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
    print("Currently saved passwords: ")
    index = 0
    for file in os.listdir(f"{password_access.userpath}/passwords/"):
        if file.endswith(".passfile"):
            index += 1
            name = file.split('.')
            print(f"{index}. {name[0]}")
    choice = input("Name of the password (Ensure it's the same as shown!): ")
    if input(f"Are you sure you want to delete {choice}? (y/n): ").lower() == "y":
        os.remove(f"{choice}.passfile")
        os.remove(f"{choice}.data")
        print(f"{choice} removed successfully!")

def generate_email():
    prefix = "https://www.1secmail.com/api/v1/"
    getmessage = "?action=getMessages"
    readMessage = "?action=readMessage"
    login = "password_manager"
    domain = "1secmail.com"
    print(f"Email is: {login}@{domain}")
    data = []
    emailids = []
    loops = 0
    while data == [] or not old:
        data = json.loads(requests.get(f"{prefix}{getmessage}&login={login}&domain={domain}").text)
        email_time = datetime.strptime(data[0]['date'], "%Y-%m-%d %H:%M:%S")
        time.sleep(5)
        if email_time < (datetime.now().replace(microsecond=0)) - timedelta(minutes=5):
            old = True
    for item in data:
        emailids.append(item["id"])
    print(emailids)
    for emailid in emailids:
        email = requests.get(f"{prefix}{readMessage}&login={login}&domain={domain}&id={emailid}")

        verif = json.loads(email.text)
        print(f"Last email sent to this address was from {email_time}:")
        print(verif['textBody'])
if __name__ == "__main__":

    generate_email()

    if not os.path.isfile("pass.hash"):
        try:
            os.mkdir(f"{password_access.userpath}/passwords/")
        except:
            pass
        print(
            "Enter your username and password. You will need to remember these to see your other passwords saved or you won't be able to!")
        

    result = ""
    while not result == "Access granted!" or result is None:
        username = input("Username: ")
        password = getpass()
        result = password_processing.password_check(username, password)
        
        if result is None:
            print("Saved your Password!")
        else:
            print(result)
    user_menu()
