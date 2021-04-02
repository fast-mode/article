from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.mdl.page import PageMdl

class Article(PageMdl):
    __tablename__ = "articles"
    status             = Column(Integer, default=1)# 0垃圾箱 1草稿箱 2已发布 3已发布不索引
    category_id        = Column(Integer, default=0)

    owner_id           = Column(Integer)

    # 想在网页上显示什么内容
    # def keys(self):
    #     return ('title','link')
    # def __getitem__(self, item):
    #     return getattr(self, item)

class List(PageMdl):
    __tablename__ = "articles_list"
    status             = Column(Integer, default=1)# 0垃圾箱 1草稿箱 2已发布 3已发布不索引

    owner_id           = Column(Integer)
