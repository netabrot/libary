from datetime import date, datetime, timezone
from typing import Any
from pydantic import BaseModel,EmailStr, SecretStr, Field, ConfigDict
from app.core.enums import UserRole