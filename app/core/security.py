from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas.token import TokenPayload
from app.core.config import settings

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_cxt.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_cxt.verify(plain_password,hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub: str = payload.get("sub")
        role: str = payload.get("role")
        if sub is None:
            raise credentials_exception
        token_data = TokenPayload(sub=sub, role = role)
    except JWTError:
        raise credentials_exception
    return token_data