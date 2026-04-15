from fastapi import FastAPI
import csv
from pathlib import Path
app = FastAPI()
user = ""

def getdict():
    u = {}
    with open('pwd.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            u[row[0]] = {
                "password": row[1],
                "admin?": row[2] == "True"
            }
    return u


def setUsers(users):
    with open('pwd.csv', 'w') as file:
        for key, inner_dict in users.items():
            line = f"{key},{inner_dict['password']},{inner_dict['admin?']}\n"
            file.write(line)
users = getdict()

@app.post('/addUser')
def addUser(a:dict):
    global user, users
    if a["setUser"]:
        if users.__contains__(a["user"]):
            users[a["user"]]={"password":a["password"],"admin?": users[a["user"]]["admin?"]}
        else:
            users[a["user"]]={"password":a["password"],"admin?":False}
        user = a["user"]
        setUsers(users)
    else:
        if users.__contains__(a["user"]):
            return {"status": "exists"}
        return {"status": ""}

@app.post('/rmUser')
def rmUser(a:dict):
    global users
    del users[a["username"]]
    setUsers(users)

@app.post('/users')
def getuser(u:dict):
    global user
    if users.__contains__(u["username"]):
        user = u["username"]
        return {"status": "exists"}
    return {"status": ""}

@app.post('/passwords')
def getuser(Pass:dict):
    if Pass["password"] == users[Pass["username"]]["password"]:
        return {"status": "loggedIn"}
    return {"status": ""}

@app.post('/changeadmin')
def pullInfo(a:dict):
    if a["request"]:
        return {"isadmin": users[a["ID"]]["admin?"]}
    else: 
        if users.__contains__(a["ID"]):
            users[a["ID"]] = {"password": users[a["ID"]]["password"], "admin?": not users[a["ID"]]["admin?"]}
            setUsers(users)
            return{"succes?": True}
        else:
            return {"succes?": False}

@app.post('/download')
def download(a:dict):
    folder = Path("users")
    files = [f.stem for f in folder.glob("*.txt")]
    if files.__contains__(a["ID"]):
        with open(f"users/{a["ID"]}.txt", "r") as f:
            lines = [line.strip() for line in f]
        return lines
    else:
        return False

@app.post('/upload')
def upload(a:dict):
    with open(f"users/{a["ID"]}.txt", "w") as f:
        for item in a["file"]:
            f.write(item + "\n")

if __name__ == "__main__":
    import uvicorn; from pathlib import Path
    uvicorn.run(f'{Path(__file__).resolve().stem}:app', host="0.0.0.0", port=8000, reload=True)
