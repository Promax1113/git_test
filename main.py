import password_processing
import password_access
import password_generator
import pathlib
import os
from getpass import getpass


def user_menu():
    menu = int(input("Press 1 for saving a password, 2 for reading a password, 3 to generate one, 4 to delete one, 5 "
                     "for settings or 6 to quit: "))

    match menu:
        case 1:
            user_save_password()
        case 2:
            user_read_password()
        case 3:
            user_generate_password()
        case 4:
            user_delete_password()
        case 5:
            user_settings()
        case _:
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
        if file.endswith(".passfile"):
            index += 1
            name = file.strip('passfile')
            print(f"{index}. {(name.strip('.'))}")
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
            name = file.strip('passfile')
            print(f"{index}. {(name.strip('.'))}")
    choice = input("Name of the password (Ensure it's the same as shown!): ")
    if input(f"Are you sure you want to delete {choice}? (y/n): ").lower() == "y":
        os.remove(f"{choice}.passfile")
        os.remove(f"{choice}.data")
        print(f"{choice} removed successfully!")


if __name__ == "__main__":

    if not os.path.isfile("pass.hash"):
        print(
            "Enter your username and password. You will need to remember these to see your other passwords saved or you won't be able to!")
        try:
            os.mkdir("/passwords/")
        except:
            pass

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
