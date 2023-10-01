#import pymongo
from fastapi import FastAPI,Response,Depends,Cookie,HTTPException
from backend.models.user import USER,login,concern
import bcrypt
from email_validator import validate_email,EmailNotValidError
import time
from fastapi.middleware.cors import CORSMiddleware

#client = pymongo.MongoClient("mongodb+srv://amankhanter14:140604@skillissue.cqzcm8a.mongodb.net/")

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://amankhanter14:140604@skillissue.cqzcm8a.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

DB = client["MUJhacks"]
user = DB["users"]
complaints = DB["complaints"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        raise HTTPException(status_code = 400,detail = "Invalid Email")
    except Exception:
        raise HTTPException(status_code = 400,detail = "Issue faced while entering data in the DB")
    return {"Message" : "Data successfully entered"}
    
@app.post("/login")
async def login(data : login,res : Response):
    data = dict(data)
    pas = data["password"]
    pas = bytes(pas,"utf-8")
    db_data = user.find_one({"email" : data["email"]},{"_id" : 0})
    if(db_data == None):
        raise HTTPException(status_code=400, detail="Email doesn't exist")
    if (bcrypt.checkpw(pas,db_data["password"])):
        print(time.time())
        res.set_cookie(key = "email",value=data["email"],expires=1200)
        return {"Message" : "Successful login"}
    else:
        raise HTTPException(status_code=400,detail="password")
    
@app.post("/concern")
def concern(con : concern, email : str = Cookie(None)):
    if email == None:
        raise HTTPException(status_code=400,detail="Re login")
    con = dict(con)
    complaints.insert_one(con)
    return {"message" : "Concern noted"}

@app.get("/concern")
def concern(email : str = Cookie(None)):
    if email == None:
        raise HTTPException(status_code=400,detail="Re login")
    all_data = complaints.find({},{"_id" : 0})
    return {"concerns" : all_data}