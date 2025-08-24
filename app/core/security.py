"""
Security
--------

Password hashing, JWT token creation, and validation.

Functions:
- get_password_hash(password)  → hash with bcrypt
- verify_password(plain, hash) → check password
- create_access_token(data)    → issue JWT with expiry
- verify_token(token, exc)     → decode JWT and return TokenPayload
"""
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas.token import TokenPayload
from app.core.config import settings
from fastapi import HTTPException, status

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_cxt.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    """Check if plain password matches the stored hash."""
    return pwd_cxt.verify(plain_password,hashed_password)

def create_access_token(subject: str, expires_delta: timedelta | None = None, additional_claims: dict | None = None):
    """Create access token."""
    expire = datetime.datetime.now() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": subject}
    if additional_claims:
        to_encode.update({k: v for k, v in additional_claims.items() if k != "sub"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> TokenPayload:
    """Decode a JWT and return the token payload (sub, role)."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub: str = payload.get("sub")
        role: str = payload.get("role")
        if sub is None:
            raise credentials_exception
        token_data = TokenPayload(sub=sub, role=role)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)    
    return token_data