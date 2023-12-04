# crud.py
from sqlalchemy.orm import Session
from models import Article
import datetime


def create_article(
    db: Session,
    title: str,
    content: str,
):
    db_article = Article(
        title=title,
        content=content,
        created_at=datetime.datetime.now(),
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Article).offset(skip).limit(limit).all()


def update_article(db: Session, article_id: int, title: str, content: str):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article:
        db_article.title = title
        db_article.content = content
        db.commit()
        db.refresh(db_article)
        return db_article
    return None


def delete_article(db: Session, article_id: int):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
        return True
    return False
