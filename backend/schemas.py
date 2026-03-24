from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class NoteCreate(BaseModel):
    title: str
    content: str


class PromptRequest(BaseModel):
    prompt: str