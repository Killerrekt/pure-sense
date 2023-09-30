import pymongo
from fastapi import FastAPI,Response,Depends,Cookie
from models.user import USER,login,concern
import bcrypt
from email_validator import validate_email,EmailNotValidError
from typing import Annotated
import time

client = pymongo.MongoClient("mongodb://localhost:27017/MUJ")
DB = client["MUJhacks"]
user = DB["users"]
complaints = DB["complaints"]

app = FastAPI()

@app.post("/signup")
async def create_user(data : USER):
    data = dict(data)
    try:
        pas = data["password"]
        pas = bytes(pas,"utf-8")
        email = validate_email(data["email"],check_deliverability=True).normalized
        if(user.find_one({"email" : data["email"]}) != None):
            return {"Error" : "Email already exist"}
        salt = bcrypt.gensalt()
        print(bcrypt.hashpw(pas,salt))
        data["password"] = bcrypt.hashpw(pas,salt)
        user.insert_one(data)
    except EmailNotValidError:
        return {"Error" : "Invalid Email"}
    except Exception:
        return {"Error" : "Issue faced while entering data in the DB"}
    return {"Message" : "Data successfully entered"}
    
@app.post("/login")
async def login(data : login,res : Response):
    data = dict(data)
    pas = data["password"]
    pas = bytes(pas,"utf-8")
    db_data = user.find_one({"email" : data["email"]},{"_id" : 0})
    if(db_data == None):
        return {"Error" : "Email doesn't exist"}
    if (bcrypt.checkpw(pas,db_data["password"])):
        print(time.time())
        res.set_cookie(key = "email",value=data["email"],expires=1200)
        return {"Message" : "Successful login"}
    else:
        return {"Error" : "Wrong Password"}
    
@app.post("/concern")
def concern(con : concern, email : str = Cookie(None)):
    if email == None:
        return {"Error" : "Re login"}
    con = dict(con)
    complaints.insert_one(con)
    return {"message" : "Concern noted"}

@app.get("/concern")
def concern(email : str = Cookie(None)):
    if email == None:
        return {"Error" : "Re login"}
    all_data = complaints.find({},{"_id" : 0})
    return {"concerns" : all_data}