from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_hours: int = 24) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=expires_hours)
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
