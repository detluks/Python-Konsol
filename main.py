import requests
ip = input("indsæt ip'en lil bro: ")
startURL = f"http://{ip}:8000"

def login():
    url = f"{startURL}/users"
    while True:
        user = input("Username: ")     
        respone = requests.post(url, json={"username": user})
        result = respone.json()
        if result["status"] == "loggedIn":
            return user
            


class User:
    def __init__(self, name):
        self.name = name


user = User(login())
print(f"du blev logget ind som:{user} lil bro")