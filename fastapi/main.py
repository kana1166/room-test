# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import authenticate_user, get_user
import crud, models, schemas
from database import engine
from session import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError

# JWTトークンの設定
SECRET_KEY = "your_secret_key"  # 実際のアプリでは安全なランダムキーを使用する
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# パスワードハッシュの設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# パスワードのハッシュ化
def hash_password(password: str):
    return pwd_context.hash(password)


# パスワードの検証
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# JWTトークンの生成
def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class OAuth2PasswordRequestFormCustom(BaseModel):
    employee_number: str
    password: str


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],  # 複数のオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JWTトークンの検証
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = get_user(db, user_id=payload["user_id"])
    if user and user.role == payload["role"]:
        return user
    raise credentials_exception


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestFormCustom = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.employee_number, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect employee number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.user_id, "role": user.role},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ユーザー関連のAPI
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if crud.delete_user(db=db, user_id=user_id):
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, updated_user=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# 会議室関連のAPI
@app.get("/rooms/", response_model=list[schemas.Room])
def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit)
    return rooms


@app.post("/rooms/", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    if crud.delete_room(db=db, room_id=room_id):
        return {"message": "Room deleted"}
    else:
        raise HTTPException(status_code=404, detail="Room not found")


@app.put("/rooms/{room_id}", response_model=schemas.Room)
def update_room(room_id: int, room: schemas.RoomUpdate, db: Session = Depends(get_db)):
    updated_room = crud.update_room(db=db, room_id=room_id, updated_room=room)
    if updated_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return updated_room


# 予約関連のAPI
@app.get("/bookings/", response_model=list[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_booking(db, skip=skip, limit=limit)
    return bookings


@app.post("/bookings/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)


@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    if crud.delete_booking(db=db, booking_id=booking_id):
        return {"message": "Booking deleted"}
    else:
        raise HTTPException(status_code=404, detail="Booking not found")


@app.put("/bookings/{booking_id}", response_model=schemas.Booking)
def update_booking(
    booking_id: int, booking: schemas.BookingUpdate, db: Session = Depends(get_db)
):
    updated_booking = crud.update_booking(
        db=db, booking_id=booking_id, updated_booking=booking
    )
    if updated_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking


# ゲストユーザー関連のAPI
@app.get("/guest_users/", response_model=list[schemas.GuestUser])
def read_guest_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    guest_users = crud.get_guest_users(db, skip=skip, limit=limit)
    return guest_users


@app.post("/guest_users/", response_model=schemas.GuestUser)
def create_guest_user(
    guest_user: schemas.GuestUserCreate, db: Session = Depends(get_db)
):
    return crud.create_guest_user(db=db, guest_user=guest_user)


@app.delete("/guest_users/{guest_user_id}")
def delete_guest_user(guest_user_id: int, db: Session = Depends(get_db)):
    if crud.delete_guest_user(db=db, guest_user_id=guest_user_id):
        return {"message": "Guest User deleted"}
    else:
        raise HTTPException(status_code=404, detail="Guest User not found")


@app.put("/guest_users/{guest_user_id}", response_model=schemas.GuestUser)
def update_guest_user(
    guest_user_id: int,
    guest_user: schemas.GuestUserUpdate,
    db: Session = Depends(get_db),
):
    updated_guest_user = crud.update_guest_user(
        db=db, guest_user_id=guest_user_id, updated_guest_user=guest_user
    )
    if updated_guest_user is None:
        raise HTTPException(status_code=404, detail="Guest User not found")
    return updated_guest_user


@app.get("/rooms/executive", response_model=list[schemas.Room])
def read_executive_rooms(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    executive_rooms = crud.get_executive_rooms(db, skip=skip, limit=limit)
    return executive_rooms


@app.post("/rooms/executive", response_model=schemas.Room)
def create_executive_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_executive_room(db=db, room=room)


@app.put("/rooms/executive/{room_id}", response_model=schemas.Room)
def update_executive_room(
    room_id: int, room: schemas.RoomUpdate, db: Session = Depends(get_db)
):
    updated_room = crud.update_executive_room(db=db, room_id=room_id, updated_room=room)
    if updated_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return updated_room


@app.delete("/rooms/executive/{room_id}")
def delete_executive_room(room_id: int, db: Session = Depends(get_db)):
    if not crud.delete_executive_room(db=db, room_id=room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted"}


@app.get("/guest_page")
def read_guest_page():
    # ゲストユーザー用のコンテンツを提供
    return {"message": "Welcome to the guest page!"}
