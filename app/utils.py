from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPExceptio, status
from fastapi.security import OAuth2PasswordBearer
from . import schemas, models, db

SECRET_KEY = "your-secret-key"
ALGORITHM = "H256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = ["auto"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str)-> bool:
    return pwd_context.verify(plain,hashed)

def create_access_token(data:dict)-> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes =ACCESS_TOKEN_EXPIRE_MINUTES )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY,algorithm = ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: db.SessionLocal = Depends(db.SessionLocal)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).get(user_id)
    if not user:
        raise credentials_exception
    return user