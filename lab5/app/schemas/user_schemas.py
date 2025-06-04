from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True
