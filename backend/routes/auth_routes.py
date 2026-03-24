from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from ..models import User
    from ..schemas import UserCreate, UserLogin
    from ..auth import hash_password, verify_password, create_access_token
    from ..database import get_db
except ImportError:
    from models import User
    from schemas import UserCreate, UserLogin
    from auth import hash_password, verify_password, create_access_token
    from database import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user.email) 
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({
        "sub": db_user.email,
        "user_id": db_user.id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }