# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from passlib.context import CryptContext
from typing import Optional, List
from pydantic import constr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ユーザーの基本情報
class UserBase(BaseModel):
    username: str = Field(max_length=12)
    role: str = Field(..., pattern="^(社員|役員|管理者)$")
    employee_number: str = Field(max_length=255)  # 社員番号の追加


# ユーザーの作成用スキーマ
class UserCreate(UserBase):
    password: str = Field(..., min_length=4)


# ユーザーの更新用スキーマ
class UserUpdate(BaseModel):
    username: Optional[str] = Field(max_length=12)
    role: Optional[str] = Field(None, pattern="^(社員|役員|管理者)$")
    password: Optional[str] = Field(None, min_length=4)
    employee_number: Optional[str] = Field(max_length=255)  # 社員番号の追加（任意）


# ユーザーの読み取り用スキーマ
class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True


# 会議室の基本情報
class RoomBase(BaseModel):
    room_name: str = Field(max_length=50)
    capacity: int
    photo_url: Optional[str] = None
    executive: bool = False


# 会議室の作成用スキーマ
class RoomCreate(RoomBase):
    pass


# 会議室の更新用スキーマ
class RoomUpdate(RoomBase):
    pass


# 会議室の読み取り用スキーマ
class Room(RoomBase):
    room_id: int

    class Config:
        orm_mode = True


# 予約の基本情報
class BookingBase(BaseModel):
    user_id: int
    room_id: int
    start_datetime: datetime
    end_datetime: datetime


# 予約の作成用スキーマ
class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    main_user_employee_number: str
    member_employee_numbers: List[str]
    guest_names: List[str]
    start_datetime: datetime
    end_datetime: datetime


# 予約の更新用スキーマ
class BookingUpdate(BookingBase):
    pass


# 予約の読み取り用スキーマ
class Booking(BookingBase):
    booking_id: int

    class Config:
        orm_mode = True


# ゲストユーザーの基本情報
class GuestUserBase(BaseModel):
    name: str = Field(max_length=255)


# ゲストユーザーの作成用スキーマ
class GuestUserCreate(GuestUserBase):
    booking_id: Optional[int] = None


# ゲストユーザーの更新用スキーマ
class GuestUserUpdate(GuestUserBase):
    booking_id: Optional[int] = None


# ゲストユーザーの読み取り用スキーマ
class GuestUser(GuestUserBase):
    guest_user_id: int
    booking_id: Optional[int] = None

    class Config:
        orm_mode = True


class Participant(BaseModel):
    name: str
    employee_number: str


class BookingWithParticipants(BaseModel):
    participants: List[Participant]
