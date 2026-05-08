from pydantic import BaseModel, EmailStr, Field

class userCreate(BaseModel):
    full_name:str
    email:EmailStr
    password:str = Field(
        min_length=8,
        max_length=72,
        description="Password must be between 8 and 72 characers"
    )
    
class UserResponse(BaseModel):
    id:int
    full_name:str
    email:EmailStr
    
    class Config:
        from_attributes = True
        
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token :str
    token_type:str
    
    