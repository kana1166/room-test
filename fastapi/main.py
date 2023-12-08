# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine
from session import SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
