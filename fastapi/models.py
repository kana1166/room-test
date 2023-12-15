# models.py
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import models as models

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    role = Column(String(255))
    password_hash = Column(String(255))
    employee_number = Column(String(255), unique=True, index=True)  # 社員番号を追加


class Room(Base):
    __tablename__ = "rooms"
    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String(255), unique=True, index=True)
    capacity = Column(Integer)
    photo_url = Column(String(255))  # 新しいカラム
    executive = Column(Boolean, default=False)  # 新しいカラム


class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    main_user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True
    )
    room_id = Column(
        Integer, ForeignKey("rooms.room_id", ondelete="SET NULL"), nullable=True
    )
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)


class BookingUsers(Base):
    __tablename__ = "booking_users"
    booking_user_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(
        Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=True
    )
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )


class GuestUser(Base):
    __tablename__ = "guest_users"
    guest_user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=True)
