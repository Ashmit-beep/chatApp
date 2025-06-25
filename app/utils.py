from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "H256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemas=["bcrypt"], deprecated = ["auto"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str)-> bool:
    return pwd_context.verify(plain,hashed)

def create_access_token(data:dict)-> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes =ACCESS_TOKEN_EXPIRE_MINUTES )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY,algorithm = ALGORITHM)
