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
            hash = hashlib.md5()
            hash.update(user.encode('utf-8'))    
            response = requests.post(url, json={"username": hash.hexdigest()})
            result = response.json()
            if result["status"] == "exists":
                break
        url = f"{startURL}/passwords"
        while True:
            Pass = input("Password: ")
            hash = hashlib.md5()
            hash.update(Pass.encode('utf-8'))
            response = requests.post(url, json={"password": hash.hexdigest()})
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

user = User(login())
print(f"du blev logget ind som:{user.name} lil bro")