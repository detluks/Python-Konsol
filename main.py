import requests
import hashlib
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
            if result["status"] == "loggedIn":
                url = f"{startURL}/addUser"
                while True:
                    password = input(f"Enter new password for {self.name}: ")
                    if password == input("Confirm new password: "):
                        p = hashlib.md5()
                        p.update(password.encode('utf-8'))
                        response = requests.post(url, json={"setUser": True,"user":u.hexdigest(), "password": p.hexdigest()})
                        break 



def main():
    user = User(login())
    print(f"du blev logget ind som:{user.name} lil bro")
    while True:
        command = input(f"{user.name}> ")
        if command == "remove user":
            if user.rmUser():
                break
        elif command == "logout":
            break  
        elif command == "passChange":
            user.passChange() 
        elif command == "help":
            print("remove user \nlogout\n")
        else:   
            print (f"'{command}' is not recognized as an command.\n")

main()