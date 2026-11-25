
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request data structure
class User(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(user: User):

    if user.username == "vishnu" and user.password == "12345":

        return {
            "status": "success",
            "message": "Login successful",
            "username": user.username
        }
    elif user.username == "vinay" and user. password == "12345":
        
        return{
            "status" : "success",
            "message": "Logged in success",
            "username" : user.username
        }

    return {
        "status": "error",
        "message": "Invalid username or password"
    }
import uvicorn 
if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)