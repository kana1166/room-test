# crud.py
from sqlalchemy.orm import Session
import models, schemas


# ユーザー一覧を取得する
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# 会議室一覧を取得する
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()


# 特定の予約をIDで取得する
def get_booking_by_id(db: Session, booking_id: int):
    return (
        db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    )


# 予約一覧を取得する
def get_booking(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


# ユーザーを登録する
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 会議室を登録する
def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(
        room_name=room.room_name,
        capacity=room.capacity,
        photo_url=room.photo_url,
        executive=room.executive,
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


# 予約を登録する
def create_booking(db: Session, booking: schemas.Booking):
    db_booking = models.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        booked_num=booking.booked_num,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


# ユーザーの役割を取得する
def get_user_role(db: Session, user_id: int) -> str:
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return user.role if user else None


# ゲストユーザーを登録する
def create_guest_user(db: Session, guest_user: schemas.GuestUserCreate):
    db_guest_user = models.GuestUser(
        name=guest_user.name,
        email=guest_user.email,
        reservation_id=guest_user.reservation_id,
    )
    db.add(db_guest_user)
    db.commit()
    db.refresh(db_guest_user)
    return db_guest_user


# ユーザーを削除する
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


# 会議室を削除する
def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if db_room:
        db.delete(db_room)
        db.commit()
        return True
    return False


# 予約を削除する
def delete_booking(db: Session, booking_id: int):
    db_booking = (
        db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    )
    if db_booking:
        db.delete(db_booking)
        db.commit()
        return True
    return False


# ゲストユーザーを削除する
def delete_guest_user(db: Session, guest_user_id: int):
    db_guest_user = (
        db.query(models.GuestUser)
        .filter(models.GuestUser.guest_user_id == guest_user_id)
        .first()
    )
    if db_guest_user:
        db.delete(db_guest_user)
        db.commit()
        return True
    return False


# ユーザーを更新する
def update_user(db: Session, user_id: int, updated_user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db_user.username = updated_user.username
        db_user.email = updated_user.email
        db_user.role = updated_user.role
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


# 会議室を更新する
def update_room(db: Session, room_id: int, updated_room: schemas.RoomUpdate):
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if db_room:
        db_room.room_name = updated_room.room_name
        db_room.capacity = updated_room.capacity
        db_room.photo_url = updated_room.photo_url
        db_room.executive = updated_room.executive
        db.commit()
        db.refresh(db_room)
        return db_room
    return None


# 予約を更新する
def update_booking(
    db: Session, booking_id: int, updated_booking: schemas.BookingUpdate
):
    db_booking = (
        db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    )
    if db_booking:
        db_booking.user_id = updated_booking.user_id
        db_booking.room_id = updated_booking.room_id
        db_booking.booked_num = updated_booking.booked_num
        db_booking.start_datetime = updated_booking.start_datetime
        db_booking.end_datetime = updated_booking.end_datetime
        db.commit()
        db.refresh(db_booking)
        return db_booking
    return None


# ゲストユーザーを更新する
def update_guest_user(
    db: Session, guest_user_id: int, updated_guest_user: schemas.GuestUserUpdate
):
    db_guest_user = (
        db.query(models.GuestUser)
        .filter(models.GuestUser.guest_user_id == guest_user_id)
        .first()
    )
    if db_guest_user:
        db_guest_user.name = updated_guest_user.name
        db_guest_user.email = updated_guest_user.email
        db_guest_user.reservation_id = updated_guest_user.reservation_id
        db.commit()
        db.refresh(db_guest_user)
        return db_guest_user
    return None
