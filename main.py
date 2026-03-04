import requests
import hashlib
startURL = "http://127.0.0.1:8000"

def login():
    url = f"{startURL}/users"
    while True:
        user = input("Username: ")
        hash = hashlib.md5()
        hash.update(user.encode('utf-8'))    
        respone = requests.post(url, json={"username": hash.hexdigest()})
        result = respone.json()
        if result["status"] == "exists":
            break
    url = f"{startURL}/passwords"
    while True:
        Pass = input("Password: ")
        hash = hashlib.md5()
        hash.update(Pass.encode('utf-8'))
        respone = requests.post(url, json={"password": hash.hexdigest()})
        result = respone.json()
        if result["status"] == "loggedIn":
            break
    return user

class User:
    def __init__(self, name):
        self.name = name

user = User(login())
print(f"du blev logget ind som:{user.name} lil bro")