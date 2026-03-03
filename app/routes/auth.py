"""
Authentication routes.

NOTE: This is a simplified auth implementation for demo purposes.
In production you'd want proper password hashing, refresh tokens,
and a real user store (database).
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from jose import jwt

from app.config import settings
from app.models.user import Token, User, UserCreate, UserLogin

router = APIRouter()

# in-memory user store (demo only)
_users: dict[str, dict] = {}


def _create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": user_id,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


@router.post("/register", response_model=User, status_code=201)
async def register(data: UserCreate):
    # check for duplicate username
    for u in _users.values():
        if u["username"] == data.username:
            raise HTTPException(status_code=409, detail="Username already taken")

    user_id = str(uuid4())
    user = {
        "id": user_id,
        "username": data.username,
        "email": data.email,
        "password": data.password,  # TODO: hash with passlib
        "created_at": datetime.now(timezone.utc),
        "is_active": True,
    }
    _users[user_id] = user

    return User(**{k: v for k, v in user.items() if k != "password"})


@router.post("/login", response_model=Token)
async def login(data: UserLogin):
    user = None
    for u in _users.values():
        if u["username"] == data.username and u["password"] == data.password:
            user = u
            break

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = _create_access_token(user["id"])
    return Token(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60,
    )
