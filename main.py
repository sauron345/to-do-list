from color_message import Message as msg
from os.path import exists
import maskpass
import json
import os


def user_authentication():
    global success_login, username
    success_login = False

    print("To-do list")
    print("Before enter the application, login/register in:")

    choice = int(input("1 - login\n2 - register\n"))

    if choice == 1:
        success_login, username = file_operations('r')

    elif choice == 2:
        file_operations('a')


def file_operations(operation: str):
    text_filename: str = 'users_data.txt'
    f = open(text_filename, operation)

    if operation == 'r':
        print("Logging in")
        username = input("Enter Username: ")
        password = maskpass.advpass()
        read_f = f.read()
        if read_f.find(username) != -1 and read_f.find(password) != -1:
            print("Logging is successfully completed")
            return True, username
        print(msg.error("Invalid username and password"))
        return False, username

    elif operation == 'w' or 'a':
        print("Registering in")
        username = input("Enter username: ")
        password = maskpass.advpass()
        f.write(f"{username}\n{password}\n\n")
        return False, username

    f.close()


def to_do_list():
    if success_login:
        if message_info:
            print(message_info)
        print(f"Welcome {username.title()} in To-do list application!")
        # CRUD features
        choice = int(input("1 - Show all my actions\n"
                           "2 - Add new action\n"
                           "3 - Remove action\n"
                           "4 - Update action\n"
                           "5 - Logout\n"))

        if choice == 1:
            try:
                actions_list = json_data[username]['actions']
                if actions_list:
                    for action in actions_list:
                        print(msg.success("- " + action))
                else:
                    message_info = msg.error(f"{username.title()} does not have any action")
            except json.decoder.JSONDecodeError:
                message_info = msg.error("File does not exist")
            except KeyError:
                message_info = msg.error(f"{username.title()} does not have any action")
            finally:
                to_do_list()

        elif choice == 2:
            action = input("Enter your action here: ")

            if username in usernames:
                json_data[username]['actions'].append(action)
            else:
                json_data[username] = {'actions': [action]}
                usernames.append(username)

            with open(json_filename, 'w') as json_f:
                json.dump(json_data, json_f, indent=4)

            message_info = print(msg.success("Your action has been successfully added"))
            to_do_list()

        elif choice == 3:
            action = input("Remove action: ")
            actions_list = json_data[username]['actions']

            if action in actions_list:
                actions_list.remove(action)
                json_data[username]['actions'] = actions_list

                with open(json_filename, 'w') as json_f:
                    json.dump(json_data, json_f, indent=4)

                message_info = msg.success("Successfully removed action")
            else:
                message_info = msg.error("Entered action not found")
            to_do_list()

        elif choice == 4:
            action = input("Name of action: ")
            actions_list = json_data[username]['actions']

            if action in actions_list:
                action_index = actions_list.index(action)
                actions_list.pop(action_index)
                new_action = input("Update the action: ")
                actions_list.insert(action_index, new_action)
                json_data[username]['actions'] = actions_list

                with open(json_filename, 'w') as json_f:
                    json.dump(json_data, json_f, indent=4)

                message_info = msg.success("Successfully updated action")
            else:
                message_info = msg.error("Entered action not found")

            to_do_list()

        elif choice == 5:
            return None

        else:
            message_info = msg.error("Invalid digit, only allowed is [1, 2, 3, 4, 5]")
            to_do_list()


def load_json_data():
    global json_data, usernames, json_filename
    json_filename = 'actions_data.json'
    json_data = {}
    usernames = []

    try:
        load_f = open(json_filename, 'r')
        json_data = json.load(load_f)
        for username_ in json_data:
            usernames.append(username_)
    except FileNotFoundError:
        return [], json_data
    except json.decoder.JSONDecodeError:
        return [], json_data
    else:
        return usernames, json_data
        load_f.close()


if __name__ == '__main__':
    global message_info
    message_info = ''
    usernames, json_data = load_json_data()

    while True:
        user_authentication()

        if success_login:
            os.system('cls')

            to_do_list()
