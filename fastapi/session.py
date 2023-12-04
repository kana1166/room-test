# session.py

from database import engine
from sqlalchemy.orm import sessionmaker

# ここで SessionLocal を定義します
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
