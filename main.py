import requests
import hashlib
from pathlib import Path
startURL = "http://127.0.0.1:8000"

def login():
    while True:
        hasUser = input("Do you have an existing acount? (y/n): ")
        if hasUser == "y" or "n":
            break
    if hasUser == "y":
        url = f"{startURL}/users"
        while True:
            user = input("Username: ")
            u = hashlib.md5()
            u.update(user.encode('utf-8'))    
            response = requests.post(url, json={"username": u.hexdigest()})
            result = response.json()
            if result["status"] == "exists":
                break
        url = f"{startURL}/passwords"
        while True:
            Pass = input("Password: ")
            p = hashlib.md5()
            p.update(Pass.encode('utf-8'))
            response = requests.post(url, json={"password": p.hexdigest(), "username": u.hexdigest()})
            result = response.json()
            if result["status"] == "loggedIn":
                break
        return user
    else: 
        url = f"{startURL}/addUser"
        while True:
            username = input("Enter new username: ")
            u = hashlib.md5()
            u.update(username.encode('utf-8'))
            response = requests.post(url, json={"setUser": False,"user":u.hexdigest()})
            result = response.json()
            if result["status"] == "":
                break
            print("username already in use")
        while True:
            password = input(f"Enter new password for {username}: ")
            if password == input("Confirm new password: "):
                p = hashlib.md5()
                p.update(password.encode('utf-8'))
                response = requests.post(url, json={"setUser": True,"user":u.hexdigest(), "password": p.hexdigest()})
                break 
        return username

class User:
    def __init__(self, name):
        self.name = name
        n = hashlib.md5()
        n.update(name.encode('utf-8'))
        self.id = n.hexdigest()
    
    def rmUser(self):
        while True:
            svar = input("are you sure you want to delete your account? (y/n): ")
            if svar == "y":
                if "confirm"== input("to delete your account please type 'confirm': "):
                    url = f"{startURL}/rmUser"
                    u = hashlib.md5()
                    u.update(self.name.encode('utf-8'))
                    requests.post(url, json={"username":u.hexdigest()})
                    return True
            elif svar == "n":
                break

    def passChange(self):
            url = f"{startURL}/passwords"
            curPass = input("Enter current password: ")
            p = hashlib.md5()
            p.update(curPass.encode('utf-8'))
            u = hashlib.md5()
            u.update(self.name.encode('utf-8'))
            response = requests.post(url, json={"password": p.hexdigest(),"username": u.hexdigest()})
            result = response.json()
            print(result)
            if result["status"] == "loggedIn":
                url = f"{startURL}/addUser"
                while True:
                    password = input(f"Enter new password for {self.name}: ")
                    if password == input("Confirm new password: "):
                        p = hashlib.md5()
                        p.update(password.encode('utf-8'))
                        response = requests.post(url, json={"setUser": True,"user":u.hexdigest(), "password": p.hexdigest()})
                        break 
    


    def changeAdmin(self):
        url = f"{startURL}/changeadmin"
        response = requests.post(url, json={"ID": self.id, "request": True})
        result = response.json()
        if result['isadmin']:
            while True:
                answer = input("Do you want to change your own acount(y/n)").lower()
                if answer == "n":
                    id = input("Enter the id of the user whose admin priviliges you'd like to change: ").lower()
                    response = requests.post(url, json={"ID": id, "request": False})
                    result = response.json()
                elif answer == "y":
                    response = requests.post(url, json={"ID": self.id, "request": False})
                    result = response.json()
                else:
                    print("you didn't enter y/n.")
                    break
                if result["succes?"]:
                    print("status changed sucsesfully!\n")
                    break
                else:
                    print("That id doesn't exist")
        else:
            print("you need admin priviliges to acces this command")        #else print you need admin priviliges to acces this command

    def upload(self):
        print("uploading...")
        url = f"{startURL}/upload"
        folder = Path("")
        files = [f.stem for f in folder.glob("*.txt")]
        if files.__contains__(self.name):
            with open(f"{self.name}.txt", "r") as f:
                lines = [line.strip() for line in f]
            requests.post(url, json={"ID": self.id,"file": lines})
            print("Upload complete!\n")
        else:
            print(f"Error file not found \nto upload a file first create a file with the name: '{self.name}.txt'")


    def download(self):
        print("downloading...")
        url = f"{startURL}/download"
        response = requests.post(url, json={"ID": self.id})
        result = response.json()
        if result:
            print(result)
            with open(f"{self.name}.txt", "w") as f:
                for item in result:
                    f.write(item + "\n")
            print("Download complete\n")
        else:
            print("This user doesn't have a file yet")
            print(f"to upload a file first create a file with the name: '{self.name}.txt'")
        
        


def main():
    user = User(login())
    print(f"you where logged in as: {user.name}")
    while True:
        command = input(f"{user.name}> ")
        if command == "remove user":
            if user.rmUser():
                break
        elif command == "logout":
            break  
        elif command == "getID":
            print(user.id)
        elif command == "download":
            user.download()
        elif command == "upload":
            user.upload()
        elif command == "changeAdmin":
            user.changeAdmin()
        elif command == "passChange":
            user.passChange() 
        elif command == "help":
            print("remove user \nlogout\n")
        else:   
            print (f"'{command}' is not recognized as an command.\n to see all commands type help")

main()