from fastapi import FastAPI
import csv
app = FastAPI()

user = ""

def getdict():
    u = {}
    with open('pwd.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            u[row[0]]={"password":row[1],"admin?":row[2]}
        return u

users = getdict()

def setUsers(users):
    with open('pwd.csv', 'w') as file:
        for key, inner_dict in users.items():
            line = f"{key},{inner_dict['password']},{inner_dict['admin?']}\n"
            file.write(line)

@app.post('/addUser')
def addUser(a:dict):
    global user, users
    if a["setUser"]:
        users[a["user"]]={"password":a["password"],"admin?":False}
        user = a["user"]
        setUsers(users)
    else:
        if users.__contains__(a["user"]):
            return {"status": "exists"}
        return {"status": ""}


@app.post('/users')
def getuser(u:dict):
    global user
    if users.__contains__(u["username"]):
        user = u["username"]
        return {"status": "exists"}
    return {"status": ""}

@app.post('/passwords')
def getuser(Pass:dict):
    if Pass["password"] == users[user]["password"]:
        return {"status": "loggedIn"}
    return {"status": ""}


if __name__ == "__main__":
    import uvicorn; from pathlib import Path
    uvicorn.run(f'{Path(__file__).resolve().stem}:app', host="0.0.0.0", port=8000, reload=True)