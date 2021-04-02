from app.models.page.crud import Page
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends,Header,Request
from .mdl import Article
from app.models.assets.crud import Assets

bp = APIRouter()
p = Page()

@bp.get('/test/{params:path}')
@p.wrap()
def test(db: Session,a,b):
    print(a)
    return "render.show(db, request, (1))"


@bp.get('/list/{params:path}')
@p.wrap()
def test(db: Session, category_id):
    context:list = db.query(Article).filter(Article.category_id == category_id).limit(10).all()
    category_data = db.query(Article).filter(Article.category_id == category)
    # 判断有无
    data = {}
    # data['image'] = Assets.path_to_link(context.image)
    data['pageData'] = context
    data['category'] = "未实现,"
    return ("article/list.html", data)