from . import BaseModel, UserRole

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str | None = None
    role: UserRole | None = None
    exp: int | None = None