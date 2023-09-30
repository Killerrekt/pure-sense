from pydantic import BaseModel

class USER(BaseModel):
    first_name : str
    last_name : str
    phone_no : int
    email : str
    password : str
    pincode : int

class login(BaseModel):
    email : str
    password : str

class concern(BaseModel):
    subject : str
    concern : str