from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import crud, models, schemas
from database import engine
from session import SessionLocal

# setup_logger 関数のインポート
from logger_config import setup_logger


logger = setup_logger()


# データベーステーブルを作成
models.Base.metadata.create_all(bind=engine)

# FastAPIのインスタンスを作成
app = FastAPI()


# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Next.jsサーバーのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Success"}


@app.post("/articles/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    new_article = crud.create_article(
        db=db, title=article.title, content=article.content
    )
    return new_article


@app.get("/articles/", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles


@app.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    return crud.get_article(db, article_id=article_id)


@app.put("/articles/{article_id}", response_model=schemas.Article)
def update_article(
    article_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)
):
    return crud.update_article(
        db=db, article_id=article_id, title=article.title, content=article.content
    )


@app.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    crud.delete_article(db=db, article_id=article_id)
    return {"detail": "Article deleted"}
