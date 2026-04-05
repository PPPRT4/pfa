from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class NoteCreate(BaseModel):
    title: str | None = None
    content: str


class NoteUpdate(BaseModel):
    content: str


class PromptRequest(BaseModel):
    prompt: str