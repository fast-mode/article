from html_builder import Html
from html_builder.Body.Image import Image
from html_builder.Body.Items import Br
from sqlalchemy import func, and_
from starlette.responses import JSONResponse

from app.models.page.crud import PageRouter, ParamsContainer, RequestItem
from fastapi import APIRouter, HTTPException, Depends, Header, Request
from enum import Enum
from sqlalchemy.orm import Session
from app.models.mdl import database
from . import orm, mdl
from app.models.user.mdl import User
from ...models.assets.crud import Assets
from ...models.system.check_token import token


def article_route(bp):
    # TODO:status 的功能

    @bp.post('/create', description='创建文章 # 1,草稿,2,发布,3,发布不索引')
    def create(
            article: orm.ArticleCreate,
            now_user: User = Depends(token.get_token_func()),
            db: Session = Depends(database.get_db)):
        now_user.into_auth("arti_edit_self")
        data_map: dict = article.dict_when_create()
        data_map['link'] = 'gg'
        # 用map新建对象,准备创建
        new_article = mdl.Article(**data_map)
        new_article.owner_id = now_user.id
        db.add(new_article)
        db.commit()
        # 改用id作为连接
        db.refresh(new_article)
        new_article.link = str(new_article.id)
        db.commit()
        return {"id": new_article.id}

    @bp.put('/update', description='更新 # 1,草稿,2,发布,3,发布不索引')
    def update(
            id: int,
            article: orm.ArticleCreate,
            now_user: User = Depends(token.get_token_func()),
            db: Session = Depends(database.get_db)):
        # 如果有编辑所有权限
        # TODO
        now_user.into_auth("arti_edit_self")
        # 增加一个更新时间戳来更新数据库
        db.query(mdl.Article) \
            .filter(mdl.Article.id == id) \
            .update(article.dict_when_update())
        db.commit()
        return True

    @bp.get('/self/ls',
            description='读取自己的文章')
    def read_self_all(
            page_index: int,
            page_size: int,
            status: int = 0,
            now_user: User = Depends(token.get_token_func()),
            db: Session = Depends(database.get_db),
    ):
        # 条件
        condition = mdl.Article.owner_id == now_user.id
        if status in {1, 2, 3}:
            condition = and_(mdl.Article.owner_id == now_user.id, mdl.Article.status == status)
        data = db.query(mdl.Article) \
            .filter(condition) \
            .offset((page_index - 1) * page_size) \
            .limit(page_size) \
            .all()
        count = db.query(func.count(mdl.Article.id)) \
            .filter(condition) \
            .scalar()
        return {
            'data': data,
            'count': count,
            'page_size': page_size,
            'page': page_index
        }

    @bp.get('/ls', description='读取所有的文章,admin的权限')
    def read_all_on_the_server(
            page_index: int,
            page_size: int,
            status: int = 0,
            now_user: User = Depends(token.check_token),
            db: Session = Depends(database.get_db),
    ):
        # 条件
        condition = mdl.Article.id > 0
        if status in {1, 2, 3}:
            condition = and_(mdl.Article.owner_id == now_user.id, mdl.Article.status == status)
        data = db.query(mdl.Article) \
            .filter(condition) \
            .offset((page_index - 1) * page_size) \
            .limit(page_size) \
            .all()
        count = db.query(func.count(mdl.Article.id)) \
            .filter(condition) \
            .scalar()
        return {
            'data': data,
            'count': count,
            'page_size': page_size,
            'page': page_index
        }

    @bp.delete('/delete', description='!')
    def delete(
            id: int,
            now_user: User = Depends(token.get_token_func()),
            db: Session = Depends(database.get_db)):
        article: mdl.Article = db.query(mdl.Article).filter(mdl.Article.id == id).first()
        if article is not None:
            article_owner_id = article.owner_id
            if article_owner_id == now_user.id:
                db.delete(article)
                db.commit()
                return {
                    'detail': 'success'
                }
            else:
                raise HTTPException(status_code=403, detail='权限不足')
        raise HTTPException(404, '文章不存在')

    # 下面是关于页面渲染的代码


def article_page_route(pg_bp, p):
    def get_show_creator():
        rt = Html('默认文章页面')
        rt.body.addElement('成功进入{{ pageData.link }}页面 图片:') \
            .addElement(Br()) \
            .addElement(Image('{{ pageData.image }}').setSize(100, 100))
        return rt

    @pg_bp.get('/show/{params:path}', description='参数只有一个:link(暂时为id)')
    @p.wrap()
    def show(pc: ParamsContainer, link: str):
        article: mdl.Article = pc.db.query(mdl.Article).filter(mdl.Article.link == link).first()
        article.reset_image_url(pc.request)
        if article is not None:
            data = {'pageData': article,
                    'prevData': article,
                    'nextData': article,
                    'category': article.category_id,
                    # 'DB_Search': self.db_search,
                    }
            return RequestItem('article/show.html', data, get_show_creator)


    def get_category_list_creator():
        rt = Html('分类列表页面')
        rt.body.addElement('成功进入分类列表页面')
        return rt

    @pg_bp.get('/list/{params:path}', description='参数有一个:category_id')
    @p.wrap()
    def list_in_category(pc: ParamsContainer, category_id: str):
        context = pc.db.query(mdl.Article).filter(mdl.Article.category_id == category_id).limit(10).all()
        data = {
            'image': "暂未有数据",
            'pageData': context,
            # 'category': self.category,
            # 'DB_Search': self.db_search
        }
        return RequestItem('article/list.html', data, get_category_list_creator)