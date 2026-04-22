import requests
import hashlib
from pathlib import Path

# Base URL til din server
startURL = "http://127.0.0.1:8000"


def login():
    # Spørg om brugeren har en konto
    while True:
        hasUser = input("Do you have an existing account? (y/n): ").lower()
        if hasUser in ["y", "n"]:   
            break

    # LOGIN (eksisterende bruger)
    if hasUser == "y":
        url = f"{startURL}/users"

        # Tjek om username findes
        while True:
            user = input("Username: ")
            u = hashlib.md5()
            u.update(user.encode('utf-8'))

            response = requests.post(url, json={"username": u.hexdigest()})
            result = response.json()

            if result["status"] == "exists":
                break
            else:
                print("User does not exist")

        # Password login
        url = f"{startURL}/passwords"
        while True:
            password = input("Password: ")
            p = hashlib.md5()
            p.update(password.encode('utf-8'))

            response = requests.post(url, json={
                "password": p.hexdigest(),
                "username": u.hexdigest()
            })
            result = response.json()

            if result["status"] == "loggedIn":
                break
            else:
                print("Wrong password")

        return user

    # REGISTER (ny bruger)
    else:
        url = f"{startURL}/addUser"

        # Opret username
        while True:
            username = input("Enter new username: ")
            u = hashlib.md5()
            u.update(username.encode('utf-8'))

            response = requests.post(url, json={
                "setUser": False,
                "user": u.hexdigest()
            })
            result = response.json()

            if result["status"] == "":
                break
            print("Username already in use")

        # Opret password
        while True:
            password = input(f"Enter new password for {username}: ")
            if password == input("Confirm new password: "):
                p = hashlib.md5()
                p.update(password.encode('utf-8'))

                requests.post(url, json={
                    "setUser": True,
                    "user": u.hexdigest(),
                    "password": p.hexdigest()
                })
                break

        return username


class User:
    def __init__(self, name):
        self.name = name

        # Generér bruger-ID via hash
        n = hashlib.md5()
        n.update(name.encode('utf-8'))
        self.id = n.hexdigest()

    def rmUser(self):
        """Sletter bruger hvis bekræftet"""
        while True:
            svar = input("Are you sure you want to delete your account? (y/n): ").lower()

            if svar == "y":
                if input("Type 'confirm' to delete your account: ") == "confirm":
                    url = f"{startURL}/rmUser"

                    u = hashlib.md5()
                    u.update(self.name.encode('utf-8'))

                    requests.post(url, json={"username": u.hexdigest()})
                    return True

            elif svar == "n":
                return False

    def passChange(self):
        """Skift password"""
        url = f"{startURL}/passwords"

        # Bekræft nuværende password
        curPass = input("Enter current password: ")
        p = hashlib.md5()
        p.update(curPass.encode('utf-8'))

        u = hashlib.md5()
        u.update(self.name.encode('utf-8'))

        response = requests.post(url, json={
            "password": p.hexdigest(),
            "username": u.hexdigest()
        })
        result = response.json()

        if result["status"] == "loggedIn":
            # Sæt nyt password
            url = f"{startURL}/addUser"
            while True:
                password = input("Enter new password: ")
                if password == input("Confirm new password: "):
                    p = hashlib.md5()
                    p.update(password.encode('utf-8'))

                    requests.post(url, json={
                        "setUser": True,
                        "user": u.hexdigest(),
                        "password": p.hexdigest()
                    })
                    print("Password changed successfully")
                    break
        else:
            print("Wrong current password")

    def changeAdmin(self):
        """Skift admin status"""
        url = f"{startURL}/changeadmin"

        response = requests.post(url, json={"ID": self.id, "request": True})
        result = response.json()

        if result['isadmin']:
            while True:
                answer = input("Change your own account? (y/n): ").lower()

                if answer == "n":
                    user_id = input("Enter user ID: ").lower()
                    response = requests.post(url, json={
                        "ID": user_id,
                        "request": False
                    })

                elif answer == "y":
                    response = requests.post(url, json={
                        "ID": self.id,
                        "request": False
                    })
                else:
                    print("Invalid input")
                    return

                result = response.json()

                if result["succes?"]:
                    print("Status changed successfully!\n")
                    break
                else:
                    print("That ID doesn't exist")
        else:
            print("You need admin privileges")

    def upload(self):
        """Uploader lokal fil"""
        print("Uploading...")
        url = f"{startURL}/upload"

        folder = Path("")
        files = [f.stem for f in folder.glob("*.txt")]

        if self.name in files:
            with open(f"{self.name}.txt", "r") as f:
                lines = [line.strip() for line in f]

            requests.post(url, json={
                "ID": self.id,
                "file": lines
            })

            Path(f"{self.name}.txt").unlink(missing_ok=True)
            print("Upload complete!\n")
        else:
            print(f"File not found: {self.name}.txt")

    def download(self):
        """Downloader fil fra server"""
        print("Downloading...")
        url = f"{startURL}/download"

        response = requests.post(url, json={"ID": self.id})
        result = response.json()

        if result:
            with open(f"{self.name}.txt", "w") as f:
                for item in result:
                    f.write(item + "\n")

            print("Download complete\n")
        else:
            print("No file found for this user")


def show_help():
    """Viser alle kommandoer"""
    print("""
Available commands:

remove user   -> Delete your account permanently
logout        -> Upload file and exit program
getID         -> Show your user ID
download      -> Download your file from server
upload        -> Upload your local file to server
changeAdmin   -> Change admin status (admin only)
passChange    -> Change your password
help          -> Show this help menu
""")


def main():
    user = User(login())

    print(f"You are logged in as: {user.name}")

    # Auto-download ved login
    user.download()

    while True:
        command = input(f"{user.name}> ").lower()

        if command == "remove user":
            if user.rmUser():
                break

        elif command == "logout":
            user.upload()
            break

        elif command == "getid":
            print(user.id)

        elif command == "download":
            user.download()

        elif command == "upload":
            user.upload()

        elif command == "changeadmin":
            user.changeAdmin()

        elif command == "passchange":
            user.passChange()

        elif command == "help":
            show_help()

        else:
            print(f"'{command}' is not a valid command. Type 'help'")


main()