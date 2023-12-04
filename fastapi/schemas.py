from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str


class Article(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True
