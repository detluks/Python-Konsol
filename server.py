from fastapi import FastAPI

app = FastAPI()

@app.post('/users')
def getuser(user:dict):
    if user["username"] == "ham":
        return {"status": "loggedIn"}
    return {"status": ""}




if __name__ == "__main__":
    import uvicorn; from pathlib import Path
    uvicorn.run(f'{Path(__file__).resolve().stem}:app', host="0.0.0.0", port=8000, reload=True)