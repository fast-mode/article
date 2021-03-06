from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Query
from app.models.mdl.page import PageOrm


# class ArticleBase(BaseModel):
#     title:           str = Query(...,min_length=1) # 不能为空的意思
#     content:         str = Query(...,min_length=1)
#     description:     Optional[str] = None
#     category_id:     Optional[int] = None
#     image:           Optional[str] = None
#     seo_title:       str = Query(...,min_length=1)
#     seo_keywords:    Optional[str] = None
#     seo_description: Optional[str] = None

class ArticleCreate(PageOrm):
    category_id: Optional[int] = None
    status: int = 1  # 1,草稿,2,发布,3,发布不索引


class Article(PageOrm):
    id: int
    owner_id: int
    category_id: int
    create_date: datetime
    update_date: datetime
    status: int

    class Config:
        orm_mode = True

# class CharaCreate(CharaBase):
