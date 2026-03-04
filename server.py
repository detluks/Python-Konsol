from fastapi import FastAPI

app = FastAPI()

users = {"79af0c177db2ee64b7301af6e1d53634": {"password":"70375478134bc7187a0d5a0ffd59c283","admin?":False},"9c5ddd54107734f7d18335a5245c286b":{"password":"0f35b3151769db9b184ade7ee5eed39c","admin?":True}}
user = ""

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