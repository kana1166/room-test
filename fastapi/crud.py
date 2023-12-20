# crud.py
from sqlalchemy.orm import Session
import models, schemas
from models import Booking, GuestUser, User
from security import verify_password, hash_password
from typing import List
from fastapi import HTTPException


# 既存のユーザー一覧を取得する関数
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


# ユーザー認証を行う関数
def authenticate_user(db: Session, employee_number: str, password: str):
    user = (
        db.query(models.User)
        .filter(models.User.employee_number == employee_number)
        .first()
    )
    if user and verify_password(password, user.password_hash):
        return user
    return None


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


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
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        role=user.role,
        employee_number=user.employee_number,  # 社員番号の追加
    )
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
def create_booking(db: Session, booking: schemas.BookingCreate):
    # 対象の部屋が役員専用かどうかを確認
    room = db.query(models.Room).filter(models.Room.room_id == booking.room_id).first()
    if room and room.executive:
        # 役員専用の部屋の場合、ユーザーが役員かどうかをチェック
        user = (
            db.query(models.User).filter(models.User.user_id == booking.user_id).first()
        )
        if not user or user.role != "役員":
            raise HTTPException(
                status_code=400, detail="Only executives can book executive rooms"
            )

    # 予約処理
    db_booking = models.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
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
        name=guest_user.name, booking_id=guest_user.booking_id
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
        if updated_user.username is not None:
            db_user.username = updated_user.username
        if updated_user.role is not None:
            db_user.role = updated_user.role
        if updated_user.password is not None:
            db_user.password_hash = hash_password(updated_user.password)
        if updated_user.employee_number is not None:
            db_user.employee_number = updated_user.employee_number  # 社員番号の更新
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
        db_guest_user.booking_id = updated_guest_user.booking_id
        db.commit()
        db.refresh(db_guest_user)
        return db_guest_user
    return None


def get_executive_rooms(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Room)
        .filter(models.Room.executive == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_executive_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(**room.dict(), executive=True)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def update_executive_room(db: Session, room_id: int, updated_room: schemas.RoomUpdate):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room is not None:
        for var, value in vars(updated_room).items():
            setattr(db_room, var, value) if value else None
        db.commit()
        db.refresh(db_room)
        return db_room
    return None


def delete_executive_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room is not None:
        db.delete(db_room)
        db.commit()
        return True
    return False


# 1. 予約を作成して自動生成された booking_id を取得
def create_booking_with_auto_generated_id(
    db: Session,
    user_id,
    room_id,
    start_datetime,
    end_datetime,
):
    new_booking = Booking(
        user_id=user_id,
        room_id=room_id,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking.booking_id  # 生成された booking_id を返す


# 2. 生成された booking_id を使用してゲストユーザーを登録
def create_guest_user_with_booking_id(db: Session, name, booking_id):
    guest_user = GuestUser(name=name, booking_id=booking_id)
    db.add(guest_user)
    db.commit()
    db.refresh(guest_user)
    return guest_user


# ゲストユーザー一覧を取得する
def get_guest_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GuestUser).offset(skip).limit(limit).all()


# 複数のゲストユーザーを登録する関数
def create_guest_users_with_booking_id(
    db: Session, guest_users: List[schemas.GuestUserCreate], booking_id: int
):
    for guest_user in guest_users:
        db_guest_user = models.GuestUser(name=guest_user.name, booking_id=booking_id)
        db.add(db_guest_user)
    db.commit()
    return (
        db.query(models.GuestUser)
        .filter(models.GuestUser.booking_id == booking_id)
        .all()
    )


# 予約時のキャパシティチェックを行う関数
def check_room_capacity(db: Session, room_id: int, number_of_guests: int) -> bool:
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if room and room.capacity >= number_of_guests:
        return True
    return False


# 予約とゲストの登録を行う関数
def create_booking_with_members(db: Session, booking_data: schemas.BookingCreate):
    # 代表者（社員）の存在チェック
    main_user = (
        db.query(models.User)
        .filter(models.User.employee_number == booking_data.main_user_employee_number)
        .first()
    )
    if not main_user:
        raise HTTPException(status_code=404, detail="Main user not found")

    # 予約の作成
    new_booking = models.Booking(
        main_user_id=main_user.user_id,
        room_id=booking_data.room_id,
        start_datetime=booking_data.start_datetime,
        end_datetime=booking_data.end_datetime,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # 追加メンバー（社員）の登録
    for employee_number in booking_data.member_employee_numbers:
        user = (
            db.query(models.User)
            .filter(models.User.employee_number == employee_number)
            .first()
        )
        if user:
            booking_user = models.BookingUsers(
                booking_id=new_booking.booking_id, user_id=user.user_id
            )
            db.add(booking_user)

    # ゲストの登録
    for guest_name in booking_data.guest_names:
        guest_user = models.GuestUser(
            name=guest_name, booking_id=new_booking.booking_id
        )
        db.add(guest_user)

    db.commit()

    return new_booking


# 特定の会議室をIDで取得する関数
def get_room_by_id(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.room_id == room_id).first()
