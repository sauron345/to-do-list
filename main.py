import maskpass
import json
import os
from color_message import Message as msg
from os.path import exists


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
    filename: str = 'users_data.txt'
    f = open(filename, operation)

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
        filename = 'actions_data.json'
        print(f"Welcome {username.title()} in To-do list application!")
        # CRUD features
        choice = int(input("1 - Show all my actions\n"
                           "2 - Add new action\n"
                           "3 - Remove action\n"
                           "4 - Update action\n"
                           "5 - Logout\n"))

        if choice == 1:
            try:
                load_f = users_actions[username]['actions']
                for action in load_f:
                    print(msg.success("- " + action))
            except json.decoder.JSONDecodeError:
                print(msg.error("File does not exist"))
            except KeyError:
                print(msg.error(f"User: {username} does not have any action"))
            finally:
                to_do_list()

        elif choice == 2:
            action = input("Enter your action here: ")

            if username in usernames:
                users_actions[username]['actions'].append(action)
            else:
                users_actions[username] = {'actions': [action]}
                usernames.append(username)

            with open(filename, 'w') as json_f:
                json.dump(users_actions, json_f, indent=4)

            print(msg.success("Your action has been successfully added"))

            to_do_list()

        elif choice == 3:
            action = input("Remove action: ")
            if action in users_actions:
                action_list.remove(action)
                with open('actions_data.json', 'a') as json_f:
                    json.dump(action_list, json_f, indent=4)
                print(msg.success("Successfully removed action"))
            else:
                print(msg.error("Entered action not found"))
            to_do_list()

        elif choice == 4:
            action = input("Name of action: ")
            with open(filename, 'r') as json_f:
                load_f = json.load(json_f)
                if action in load_f:
                    action_list: list = load_f[username]['actions']
                    action_index = action_list.index(action)
                    action_list.pop(action_index)
                    new_action = input("Update the action: ")
                    action_list.insert(action_index, new_action)
                    print(msg.success("Successfully removed action"))
                else:
                    print(msg.error("Entered action not found"))
            to_do_list()

        elif choice == 5:
            return None

        else:
            print(msg.error("Invalid digit, only allowed is [1, 2, 3, 4, 5]"))
            to_do_list()


def load_json_data():
    global users_actions
    try:
        load_f = open('actions_data.json', 'w+')
        json_data = json.load(load_f)
        for username_ in json_data:
            usernames.append(username_)
    except json.decoder.JSONDecodeError:
        users_actions = {}
        return [], users_actions
    else:
        return usernames, json_data
    finally:
        load_f.close()


if __name__ == '__main__':
    usernames = []
    usernames, users_actions = load_json_data()

    while True:
        user_authentication()

        if success_login:
            os.system('cls')

            to_do_list()
